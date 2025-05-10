/*
 * Advanced TCP Server with Buffer Overflow Vulnerability
 * 
 * This program demonstrates a classic buffer overflow vulnerability in a TCP server.
 * It contains a vulnerable function that doesn't properly check input length,
 * allowing an attacker to overwrite the stack and execute arbitrary code.
 *
 * Compile with: gcc -o tcpserver-basic tcpserver-basic.c -fno-stack-protector -z execstack
 *
 * Security features deliberately disabled:
 * - Stack canaries (-fno-stack-protector)
 * - Executable stack (-z execstack)
 * - ASLR should be disabled at runtime: echo 0 > /proc/sys/kernel/randomize_va_space
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <signal.h>

#define DEFAULT_PORT 9999
#define BUFFER_SIZE 128

int server_sock;

/* Signal handler to properly close the server socket */
void handle_signal(int sig) {
    printf("\nCaught signal %d. Shutting down...\n", sig);
    if (server_sock) close(server_sock);
    exit(0);
}

/* Vulnerable function with buffer overflow */
void handle_client(int client_sock) {
    char buffer[BUFFER_SIZE];
    ssize_t bytes_received;
    
    /* Clear the buffer */
    memset(buffer, 0, BUFFER_SIZE);
    
    /* Receive data from client - VULNERABLE: no size checking */
    bytes_received = recv(client_sock, buffer, 1024, 0);  // Deliberately receiving more than buffer size
    
    if (bytes_received > 0) {
        printf("Received %zd bytes from client\n", bytes_received);
        
        /* Echo back to client - this likely won't execute if exploited */
        send(client_sock, buffer, bytes_received, 0);
    }
    
    /* Function returns here, but if buffer overflow occurs, 
       the return address will be overwritten and execution will jump elsewhere */
}

/* Advanced server implementation with proper error handling */
int main(int argc, char *argv[]) {
    int port = DEFAULT_PORT;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);
    int client_sock;
    
    /* Allow custom port via command line argument */
    if (argc > 1) {
        port = atoi(argv[1]);
        if (port <= 0 || port > 65535) {
            fprintf(stderr, "Error: Invalid port number. Using default port %d\n", DEFAULT_PORT);
            port = DEFAULT_PORT;
        }
    }
    
    /* Set up signal handlers for clean shutdown */
    signal(SIGINT, handle_signal);
    signal(SIGTERM, handle_signal);
    
    /* Create socket */
    server_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (server_sock < 0) {
        perror("Error creating socket");
        return 1;
    }
    
    /* Set socket options to reuse address */
    int opt = 1;
    if (setsockopt(server_sock, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        perror("Error setting socket options");
        close(server_sock);
        return 1;
    }
    
    /* Configure server address */
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);
    
    /* Bind socket */
    if (bind(server_sock, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Error binding socket");
        close(server_sock);
        return 1;
    }
    
    /* Listen for connections */
    if (listen(server_sock, 5) < 0) {
        perror("Error listening");
        close(server_sock);
        return 1;
    }
    
    printf("[+] Server started on port %d\n", port);
    printf("[+] Waiting for connections...\n");
    printf("[!] WARNING: This server contains a deliberate buffer overflow vulnerability!\n");
    
    /* Main server loop */
    while (1) {
        /* Accept connection */
        client_sock = accept(server_sock, (struct sockaddr *)&client_addr, &client_len);
        if (client_sock < 0) {
            perror("Error accepting connection");
            continue;
        }
        
        printf("[+] Connection from %s:%d\n", 
               inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
        
        /* Handle client in the same process - vulnerable to buffer overflow */
        handle_client(client_sock);
        
        /* Close client socket */
        close(client_sock);
        printf("[+] Connection closed\n");
    }
    
    /* This code is never reached, but included for completeness */
    close(server_sock);
    return 0;
}