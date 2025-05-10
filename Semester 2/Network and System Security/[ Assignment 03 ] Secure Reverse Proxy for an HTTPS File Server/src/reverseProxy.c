#include "tlsServer.h"
#include "pamAuth.h"
#include "httpClient.h"
#include "utils.h"
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

SSL_CTX* globalCtx;

void commandLoop(SSL* ssl);

void* handleClient(void* arg) {
    int clientFd = (int)(intptr_t)arg;
    SSL* ssl = SSL_new(globalCtx);
    SSL_set_fd(ssl, clientFd);

    if (SSL_accept(ssl) <= 0) {
        logError("SSL_accept failed");
        SSL_free(ssl);
        close(clientFd);
        return NULL;
    }

    if (handleLogin(ssl)) {
        commandLoop(ssl);
    }

    SSL_shutdown(ssl);
    SSL_free(ssl);
    close(clientFd);
    return NULL;
}

void commandLoop(SSL* ssl) {
    char buffer[1024];
    while (1) {
        sendMessage(ssl, "HTTPS_SERVER> ");
        int len = receiveMessage(ssl, buffer, sizeof(buffer));
        if (len <= 0) break;

        buffer[len] = '\0';
        char* command = strtok(buffer, " \n");
        if (!command) continue;

        if (strcmp(command, "exit") == 0) {
            break;
        } else if (strcmp(command, "ls") == 0) {
            listFiles(ssl);
        } else if (strcmp(command, "get") == 0) {
            char* filename = strtok(NULL, " \n");
            if (filename) getFile(ssl, filename);
            else sendMessage(ssl, "ERROR Missing filename\n");
        } else if (strcmp(command, "put") == 0) {
            char* filename = strtok(NULL, " \n");
            char* sizeStr = strtok(NULL, " \n");
            if (filename && sizeStr) putFile(ssl, filename, atoi(sizeStr));
            else sendMessage(ssl, "ERROR Missing filename or size\n");
        } else {
            sendMessage(ssl, "ERROR Unknown command\n");
        }
    }
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
        if (pthread_create(&thread, NULL, handleClient, (void*)(intptr_t)clientFd) != 0) {
            close(clientFd);
        }
        pthread_detach(thread);
    }

    SSL_CTX_free(globalCtx);
    close(serverFd);
    return 0;
}
