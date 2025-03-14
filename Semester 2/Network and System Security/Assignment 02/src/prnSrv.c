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

    // Get printer server key
    unsigned char prnKey[KEY_LEN] = {0}, salt[SALT_LEN] = {0};
    memcpy(salt, KDC_SALT, SALT_LEN);
    deriveKey("prn_password", salt, prnKey);

    // Receive nonce from client
    unsigned char nonce[NONCE_LEN] = {0};
    if (read(clientSock, nonce, NONCE_LEN) <= 0) {
        perror("Read nonce failed");
        close(clientSock);
        free(args);
        return NULL;
    }

    // Receive filename
    char filename[256] = {0};
    ssize_t bytesRead = read(clientSock, filename, sizeof(filename) - 1);
    if (bytesRead <= 0) {
        perror("Read failed");
        close(clientSock);
        free(args);
        return NULL;
    }

    // Extract K_AP from ticket (simplified for now)
    // In a real implementation, we would validate the ticket received from the client
    unsigned char kap[KEY_LEN] = {0};
    deriveKey("session_key", salt, kap); // This is a placeholder

    // Determine file type and convert to PDF
    char command[512] = {0};
    char *fileExt = strrchr(filename, '.'); // Get file extension

    if (fileExt != NULL && strcmp(fileExt, ".txt") == 0) {
        // Convert text to PDF using enscript + ps2pdf
        snprintf(command, sizeof(command), 
                 "enscript %s -o - | ps2pdf - output.pdf", filename);
    } else {
        // Default to img2pdf for images
        snprintf(command, sizeof(command), 
                 "img2pdf %s -o output.pdf", filename);
    }

    // Execute conversion command
    int ret = system(command);
    if (ret != 0) {
        fprintf(stderr, "Conversion failed for file: %s\n", filename);
        close(clientSock);
        free(args);
        return NULL;
    }

    // Encrypt and send PDF
    FILE *pdf = fopen("output.pdf", "rb");
    if (pdf == NULL) {
        perror("Failed to open PDF");
        close(clientSock);
        free(args);
        return NULL;
    }

    fseek(pdf, 0, SEEK_END);
    long size = ftell(pdf);
    fseek(pdf, 0, SEEK_SET);
    
    unsigned char *pdfData = malloc(size);
    if (pdfData == NULL) {
        perror("Failed to allocate memory");
        fclose(pdf);
        close(clientSock);
        free(args);
        return NULL;
    }

    if (fread(pdfData, 1, size, pdf) != (size_t)size) {
        perror("Failed to read PDF file");
        free(pdfData);
        fclose(pdf);
        close(clientSock);
        free(args);
        return NULL;
    }
    fclose(pdf);

    // Encrypt PDF with session key
    unsigned char *encryptedPdf = malloc(size);
    unsigned char tag[TAG_LEN] = {0};
    
    if (encryptedPdf == NULL) {
        perror("Failed to allocate memory for encrypted PDF");
        free(pdfData);
        close(clientSock);
        free(args);
        return NULL;
    }
    
    encryptData(pdfData, size, kap, nonce, encryptedPdf, tag);
    
    // Send encrypted PDF
    if (write(clientSock, encryptedPdf, size) <= 0) {
        perror("Write PDF failed");
        free(encryptedPdf);
        free(pdfData);
        close(clientSock);
        free(args);
        return NULL;
    }
    
    // Send tag separately
    if (write(clientSock, tag, TAG_LEN) <= 0) {
        perror("Write tag failed");
        free(encryptedPdf);
        free(pdfData);
        close(clientSock);
        free(args);
        return NULL;
    }

    free(encryptedPdf);
    free(pdfData);
    close(clientSock);
    free(args);
    logMessage("File processed and sent successfully");
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
        .sin_port = htons(PRN_PORT),
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

    printf("[Print Server] Listening on port %d...\n", PRN_PORT);

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
