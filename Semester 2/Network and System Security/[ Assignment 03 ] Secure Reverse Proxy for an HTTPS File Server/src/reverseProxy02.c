#include "tlsServer.h"
#include "pamAuth.h"
#include "httpClient.h"
#include "utils.h"
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#ifdef __linux__
#include <sched.h>
#endif

SSL_CTX* globalCtx;

void* handleClient(void* arg) {
    int clientFd = (int)(intptr_t)arg;
    SSL* ssl = SSL_new(globalCtx);
    if (!ssl) {
        logError("Failed to create SSL object");
        close(clientFd);
        return NULL;
    }
    SSL_set_fd(ssl, clientFd);

    if (SSL_accept(ssl) <= 0) {
        logError("TLS handshake failed");
        SSL_free(ssl);
        close(clientFd);
        return NULL;
    }

    if (handleLogin(ssl)) {
        char buffer[1024];
        while (1) {
            if (sendMessage(ssl, "HTTPS_SERVER> ") <= 0) {
                logError("Failed to send prompt");
                break;
            }
            int len = receiveMessage(ssl, buffer, sizeof(buffer));
            if (len <= 0) {
                logError("Client disconnected");
                break;
            }

            buffer[len] = '\0';
            char* command = strtok(buffer, " ");
            if (!command) continue;

            if (strcmp(command, "exit") == 0) {
                break;
            } else if (strcmp(command, "ls") == 0) {
                listFiles(ssl);
            } else if (strcmp(command, "get") == 0) {
                char* filename = strtok(NULL, " ");
                if (filename && !strtok(NULL, " ")) {
                    getFile(ssl, filename);
                } else {
                    sendMessage(ssl, "ERROR: Syntax: get <filename>\n");
                }
            } else if (strcmp(command, "put") == 0) {
                char* filename = strtok(NULL, " ");
                char* sizeStr = strtok(NULL, " ");
                if (filename && sizeStr && !strtok(NULL, " ")) {
                    int size = atoi(sizeStr);
                    if (size > 0) {
                        putFile(ssl, filename, size);
                    } else {
                        sendMessage(ssl, "ERROR: Invalid size\n");
                    }
                } else {
                    sendMessage(ssl, "ERROR: Syntax: put <filename> <size>\n");
                }
            } else {
                sendMessage(ssl, "ERROR: Unknown command\n");
            }
        }
    }

    SSL_shutdown(ssl);
    SSL_free(ssl);
    close(clientFd);
    return NULL;
}

int main() {
    globalCtx = setupTlsServer("certs/reverse_proxy.crt", "certs/reverse_proxy.key");
    if (!globalCtx) {
        fprintf(stderr, "Failed to setup TLS server\n");
        return 1;
    }

    int serverFd = setupServerSocket(8443);
    if (serverFd < 0) {
        SSL_CTX_free(globalCtx);
        return 1;
    }

    while (1) {
        int clientFd = acceptClient(serverFd);
        if (clientFd < 0) continue;

        pthread_t thread;
        pthread_attr_t attr;
        pthread_attr_init(&attr);
        pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED);
        if (pthread_create(&thread, &attr, handleClient, (void*)(intptr_t)clientFd) != 0) {
            logError("Failed to create thread");
            close(clientFd);
        }
        pthread_attr_destroy(&attr);
    }

    SSL_CTX_free(globalCtx);
    close(serverFd);
    return 0;
}