#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <openssl/rand.h>
#include "cryptoUtils.h"
#include "config.h"
#include "logger.h"

typedef struct {
    int socket;
} clientArgs;

void *handleClient(void *arg) {
    clientArgs *args = (clientArgs *)arg;
    int clientSock = args->socket;

    // Simplified authentication
    char username[256] = {0};
    ssize_t bytesRead = read(clientSock, username, sizeof(username) - 1);
    if (bytesRead <= 0) {
        perror("Read failed");
        close(clientSock);
        free(args);
        return NULL;
    }
    
    printf("[KDC] Received authentication request from: %s\n", username);

    // Derive client key
    unsigned char clientKey[KEY_LEN] = {0}, salt[SALT_LEN] = {0};
    memcpy(salt, KDC_SALT, SALT_LEN);
    deriveKey("alice_password", salt, clientKey);

    // Generate session key K_AP
    unsigned char kap[KEY_LEN] = {0};
    if (RAND_bytes(kap, KEY_LEN) != 1) {
        perror("Failed to generate session key");
        close(clientSock);
        free(args);
        return NULL;
    }
    
    printf("[KDC] Generated session key for %s\n", username);

    // Generate nonce for client communication
    unsigned char nonce[NONCE_LEN] = {0};
    generateNonce(nonce);
    
    // Encrypt session key for client
    unsigned char encSessionKey[KEY_LEN] = {0};
    unsigned char tag[TAG_LEN] = {0};
    
    encryptData(kap, KEY_LEN, clientKey, nonce, encSessionKey, tag);
    
    printf("[KDC] Encrypted session key with client key\n");

    // Send nonce
    if (write(clientSock, nonce, NONCE_LEN) <= 0) {
        perror("Write nonce failed");
        close(clientSock);
        free(args);
        return NULL;
    }
    
    // Send encrypted session key
    if (write(clientSock, encSessionKey, KEY_LEN) <= 0) {
        perror("Write session key failed");
        close(clientSock);
        free(args);
        return NULL;
    }
    
    // Send authentication tag
    if (write(clientSock, tag, TAG_LEN) <= 0) {
        perror("Write tag failed");
        close(clientSock);
        free(args);
        return NULL;
    }
    
    printf("[KDC] Sent encrypted session key and tag to client\n");

    close(clientSock);
    free(args);
    logMessage("Client handled successfully");
    return NULL;
}

int main() {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("Socket creation failed");
        return 1;
    }

    // Allow socket reuse to prevent "Address already in use" errors
    int opt = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        perror("Setsockopt failed");
        close(sock);
        return 1;
    }

    struct sockaddr_in addr = {
        .sin_family = AF_INET,
        .sin_port = htons(KDC_PORT),
        .sin_addr.s_addr = INADDR_ANY
    };

    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("Bind failed");
        close(sock);
        return 1;
    }

    if (listen(sock, MAX_CLIENTS) < 0) {
        perror("Listen failed");
        close(sock);
        return 1;
    }

    printf("[KDC Server] Listening on port %d...\n", KDC_PORT);

    while (1) {
        int clientSock = accept(sock, NULL, NULL);
        if (clientSock < 0) {
            perror("Accept failed");
            continue;
        }

        clientArgs *args = malloc(sizeof(clientArgs));
        if (args == NULL) {
            perror("Failed to allocate memory");
            close(clientSock);
            continue;
        }

        args->socket = clientSock;
        pthread_t thread;
        if (pthread_create(&thread, NULL, handleClient, args) != 0) {
            perror("Failed to create thread");
            close(clientSock);
            free(args);
        }
    }

    close(sock);
    return 0;
}