#include "tlsClient.h"
#include "utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>
#ifdef __FreeBSD__
#include <sys/wait.h>
#endif

void disableEcho() {
    struct termios tty;
    tcgetattr(STDIN_FILENO, &tty);
    tty.c_lflag &= ~ECHO;
    tcsetattr(STDIN_FILENO, TCSANOW, &tty);
}

void enableEcho() {
    struct termios tty;
    tcgetattr(STDIN_FILENO, &tty);
    tty.c_lflag |= ECHO;
    tcsetattr(STDIN_FILENO, TCSANOW, &tty);
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <host>\n", argv[0]);
        return 1;
    }
    const char* host = argv[1];

    SSL_CTX* ctx = setupTlsClient("certs/ca.crt", NULL);
    if (!ctx) {
        logError("TLS client setup failed");
        return 1;
    }

    int sock = connectToServer(host, 8443);
    if (sock < 0) {
        SSL_CTX_free(ctx);
        return 1;
    }

    SSL* ssl = SSL_new(ctx);
    if (!ssl) {
        logError("Failed to create SSL object");
        close(sock);
        SSL_CTX_free(ctx);
        return 1;
    }
    SSL_set_fd(ssl, sock);

    if (SSL_connect(ssl) <= 0) {
        logError("TLS handshake failed (invalid certificate or server error)");
        SSL_free(ssl);
        close(sock);
        SSL_CTX_free(ctx);
        return 1;
    }

    char buffer[1024];
    int len = receiveMessage(ssl, buffer, sizeof(buffer));
    if (len <= 0) {
        logError("Failed to receive username prompt");
        goto cleanup;
    }
    printf("%s", buffer);
    if (fgets(buffer, sizeof(buffer), stdin) == NULL) {
        logError("Failed to read username");
        goto cleanup;
    }
    sendMessage(ssl, buffer);

    len = receiveMessage(ssl, buffer, sizeof(buffer));
    if (len <= 0) {
        logError("Failed to receive password prompt");
        goto cleanup;
    }
    printf("%s", buffer);
    disableEcho();
    if (fgets(buffer, sizeof(buffer), stdin) == NULL) {
        logError("Failed to read password");
        enableEcho();
        goto cleanup;
    }
    enableEcho();
    sendMessage(ssl, buffer);

    len = receiveMessage(ssl, buffer, sizeof(buffer));
    if (len <= 0 || strcmp(buffer, "HTTPS_SERVER> ") != 0) {
        printf("ERROR: Authentication failed or server error\n");
        goto cleanup;
    }

    printf("%s", buffer);
    while (1) {
        if (fgets(buffer, sizeof(buffer), stdin) == NULL) {
            printf("ERROR: Failed to read command\n");
            break;
        }
        buffer[strcspn(buffer, "\n")] = '\0';
        char* cmd = strtok(buffer, " ");
        if (!cmd) {
            printf("ERROR: Empty command\nHTTPS_SERVER> ");
            continue;
        }

        if (strcmp(cmd, "get") == 0) {
            char* filename = strtok(NULL, " ");
            if (!filename || strtok(NULL, " ")) {
                printf("ERROR: Syntax: get <filename>\nHTTPS_SERVER> ");
                continue;
            }
        } else if (strcmp(cmd, "put") == 0) {
            char* filename = strtok(NULL, " ");
            char* size_str = strtok(NULL, " ");
            if (!filename || !size_str || strtok(NULL, " ")) {
                printf("ERROR: Syntax: put <filename> <size>\nHTTPS_SERVER> ");
                continue;
            }
            int size = atoi(size_str);
            if (size <= 0) {
                printf("ERROR: Invalid size\nHTTPS_SERVER> ");
                continue;
            }
        } else if (strcmp(cmd, "ls") != 0 && strcmp(cmd, "exit") != 0) {
            printf("ERROR: Unknown command\nHTTPS_SERVER> ");
            continue;
        }

        sendMessage(ssl, buffer);
        if (strcmp(cmd, "put") == 0) {
            char* filename = strtok(NULL, " ");
            char* size_str = strtok(NULL, " ");
            int size = atoi(size_str);
            printf("Enter %d bytes for %s: ", size, filename);
            char* content = malloc(size + 1);
            if (!content) {
                printf("ERROR: Memory allocation failed\nHTTPS_SERVER> ");
                continue;
            }
            int read_bytes = fread(content, 1, size, stdin);
            if (read_bytes != size) {
                printf("ERROR: Expected %d bytes, got %d\nHTTPS_SERVER> ", size, read_bytes);
                free(content);
                continue;
            }
            content[size] = '\0';
            if (SSL_write(ssl, content, size) <= 0) {
                printf("ERROR: Failed to send file content\n");
                free(content);
                break;
            }
            free(content);
            int c;
            while ((c = getchar()) != '\n' && c != EOF);
        }

        while (1) {
            len = receiveMessage(ssl, buffer, sizeof(buffer));
            if (len <= 0) {
                printf("ERROR: Server disconnected\n");
                goto cleanup;
            }
            buffer[len] = '\0';
            if (strncmp(buffer, "OK", 2) == 0 && strcmp(cmd, "get") == 0) {
                char* filename = strtok(buffer + 3, " ");
                handleFileDownload(ssl, buffer, filename ? filename : "downloaded_file");
                printf("File downloaded successfully\nHTTPS_SERVER> ");
                break;
            } else if (strcmp(buffer, "END\n") == 0 || strcmp(buffer, "HTTPS_SERVER> ") == 0) {
                printf("%s", buffer);
                break;
            } else {
                printf("%s", buffer);
            }
        }
        if (strcmp(cmd, "exit") == 0) break;
    }

cleanup:
    if (ssl) {
        SSL_shutdown(ssl);
        SSL_free(ssl);
    }
    if (sock >= 0) close(sock);
    SSL_CTX_free(ctx);
    return 0;
}