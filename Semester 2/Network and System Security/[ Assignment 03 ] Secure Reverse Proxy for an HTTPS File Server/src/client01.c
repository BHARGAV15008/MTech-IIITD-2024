#include "tlsClient.h"
#include "utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>

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

int main() {
    SSL_CTX* ctx = setupTlsClient("certs/ca.crt");
    if (!ctx) {
        logError("Failed to setup TLS client");
        return 1;
    }

    int sock = connectToServer("192.168.118.131", 8443);
    if (sock < 0) {
        logError("Failed to connect to server");
        SSL_CTX_free(ctx);
        return 1;
    }

    SSL* ssl = SSL_new(ctx);
    SSL_set_fd(ssl, sock);
    if (SSL_connect(ssl) <= 0) {
        logError("SSL_connect failed");
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
    fgets(buffer, sizeof(buffer), stdin);
    sendMessage(ssl, buffer);

    len = receiveMessage(ssl, buffer, sizeof(buffer));
    if (len <= 0) {
        logError("Failed to receive password prompt");
        goto cleanup;
    }
    printf("%s", buffer);
    disableEcho();
    fgets(buffer, sizeof(buffer), stdin);
    enableEcho();
    sendMessage(ssl, buffer);

    len = receiveMessage(ssl, buffer, sizeof(buffer));
    if (len <= 0 || strcmp(buffer, "HTTPS_SERVER> ") != 0) {
        logError("Login failed or unexpected server response");
        goto cleanup;
    }

    printf("%s", buffer);
    while (1) {
        fgets(buffer, sizeof(buffer), stdin);
        char command[1024];
        strcpy(command, buffer);
        char* cmd = strtok(command, " \n");
        if (!cmd) {
            printf("ERROR Empty command\n");
            printf("HTTPS_SERVER> ");
            continue;
        }

        // Validate commands locally
        if (strcmp(cmd, "get") == 0) {
            char* filename = strtok(NULL, " \n");
            char* extra = strtok(NULL, " \n");
            if (!filename || extra) {
                printf("ERROR Invalid get syntax: get <filename>\n");
                printf("HTTPS_SERVER> ");
                continue;
            }
        } else if (strcmp(cmd, "put") == 0) {
            char* filename = strtok(NULL, " \n");
            char* size_str = strtok(NULL, " \n");
            char* extra = strtok(NULL, " \n");
            if (!filename || !size_str || extra) {
                printf("ERROR Invalid put syntax: put <filename> <size>\n");
                printf("HTTPS_SERVER> ");
                continue;
            }
        }

        // Send command
        sendMessage(ssl, buffer);

        // Handle 'put' data
        if (strcmp(cmd, "put") == 0) {
            char* filename = strtok(NULL, " \n");
            char* size_str = strtok(NULL, " \n");
            if (filename && size_str) {
                int size = atoi(size_str);
                if (size <= 0) {
                    printf("ERROR Invalid size\n");
                    continue;
                }
                printf("Enter exactly %d bytes for %s: ", size, filename);
                char* content = malloc(size + 1);
                int read_bytes = 0;
                while (read_bytes < size) {
                    int c = getchar();
                    if (c == EOF || c == '\n') break;
                    content[read_bytes++] = c;
                }
                if (read_bytes != size) {
                    printf("ERROR Entered %d bytes, expected %d\n", read_bytes, size);
                    free(content);
                    continue;
                }
                content[size] = '\0';
                SSL_write(ssl, content, size);
                free(content);
            }
        }

        // Receive response
        while (1) {
            len = receiveMessage(ssl, buffer, sizeof(buffer));
            if (len <= 0) {
                logError("Connection closed by server");
                goto cleanup;
            }
            buffer[len] = '\0';

            if (strstr(buffer, "OK") == buffer) {
                if (strcmp(cmd, "get") == 0) {
                    handleFileDownload(ssl, buffer);
                }
                printf("%s", buffer);
                printf("HTTPS_SERVER> ");
                fflush(stdout);
                break;
            } else if (strcmp(buffer, "END\n") == 0) {
                printf("HTTPS_SERVER> ");
                fflush(stdout);
                break;
            } else if (strcmp(buffer, "HTTPS_SERVER> ") == 0) {
                printf("%s", buffer);
                fflush(stdout);
                break;
            } else {
                // Avoid displaying raw HTML
                if (strstr(buffer, "<html>")) {
                    printf("ERROR Server error\n");
                } else {
                    printf("%s", buffer);
                }
            }
        }
    }

cleanup:
    SSL_shutdown(ssl);
    SSL_free(ssl);
    close(sock);
    SSL_CTX_free(ctx);
    return 0;
}