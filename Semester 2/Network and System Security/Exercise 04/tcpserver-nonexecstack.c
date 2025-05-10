/*
 * Advanced TCP Server with Buffer Overflow Vulnerability (Non-Executable Stack)
 * 
 * This program demonstrates a buffer overflow vulnerability in a TCP server
 * with non-executable stack protection enabled. This requires more advanced
 * exploitation techniques like Return-Oriented Programming (ROP).
 *
 * Compile with: gcc -o tcpserver-nonexecstack tcpserver-nonexecstack.c -fno-stack-protector
 *
 * Security features:
 * - Non-executable stack is ENABLED (default in modern systems)
 * - Stack canaries are disabled (-fno-stack-protector)
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

#define DEFAULT_PORT 9998
#define BUFFER_SIZE 128

int server_sock;

/* Some dummy functions that could be used in ROP chains */
/* Using architecture-specific assembly for compatibility */
#if defined(__x86_64__) || defined(_M_X64)
/* 64-bit architecture */
void dummy_function1(void) {
    asm("pop %rax\n"
        "ret");
}

void dummy_function2(void) {
    asm("pop %rbx\n"
        "ret");
}

void dummy_function3(void) {
    asm("pop %rcx\n"
        "ret");
}
#else
/* 32-bit architecture */
void dummy_function1(void) {
    asm("pop %eax\n"
        "ret");
}

void dummy_function2(void) {
    asm("pop %ebx\n"
        "ret");
}

void dummy_function3(void) {
    asm("pop %ecx\n"
        "ret");
}
#endif

void dummy_function4(void) {
    asm("int $0x80\n"
        "ret");
}

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

/* Print addresses of ROP gadgets for educational purposes */
void print_rop_gadgets(void) {
    printf("[*] ROP Gadget Addresses (for educational purposes):\n");
#if defined(__x86_64__) || defined(_M_X64)
    printf("    dummy_function1: %p (pop rax; ret)\n", dummy_function1);
    printf("    dummy_function2: %p (pop rbx; ret)\n", dummy_function2);
    printf("    dummy_function3: %p (pop rcx; ret)\n", dummy_function3);
#else
    printf("    dummy_function1: %p (pop eax; ret)\n", dummy_function1);
    printf("    dummy_function2: %p (pop ebx; ret)\n", dummy_function2);
    printf("    dummy_function3: %p (pop ecx; ret)\n", dummy_function3);
#endif
    printf("    dummy_function4: %p (int 0x80; ret)\n", dummy_function4);
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
    printf("[!] Non-executable stack protection is ENABLED\n");
    
    /* Print ROP gadget addresses for educational purposes */
    print_rop_gadgets();
    
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