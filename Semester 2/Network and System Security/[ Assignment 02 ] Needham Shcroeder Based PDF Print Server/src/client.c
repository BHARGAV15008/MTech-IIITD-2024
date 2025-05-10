#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <openssl/rand.h>
#include "cryptoUtils.h"
#include "config.h"
#include "logger.h"

void connectToPrintServer(unsigned char *kap, const unsigned char *nonce, const char *filename, const char *server_ip) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        perror("Socket creation failed");
        return;
    }

    struct sockaddr_in addr = {
        .sin_family = AF_INET, 
        .sin_port = htons(PRN_PORT), 
        .sin_addr.s_addr = inet_addr(server_ip)
    };
    if (connect(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("Connection failed");
        close(sock);
        return;
    }
    
    printf("[Client] Connected to print server\n");

    // Send nonce
    if (write(sock, nonce, NONCE_LEN) <= 0) {
        perror("Write nonce failed");
        close(sock);
        return;
    }
    
    printf("[Client] Sent nonce to print server\n");

    // Send filename
    if (write(sock, filename, strlen(filename) + 1) <= 0) {
        perror("Write filename failed");
        close(sock);
        return;
    }
    
    printf("[Client] Sent filename '%s' to print server\n", filename);

    // Receive encrypted PDF size first
    uint32_t pdfSize = 0;
    if (read(sock, &pdfSize, sizeof(pdfSize)) <= 0) {
        perror("Read PDF size failed");
        close(sock);
        return;
    }
    
    pdfSize = ntohl(pdfSize); // Convert from network byte order
    printf("[Client] Receiving PDF of size: %u bytes\n", pdfSize);
    
    // Allocate memory for encrypted PDF
    unsigned char *encryptedPdf = malloc(pdfSize);
    if (!encryptedPdf) {
        perror("Memory allocation failed");
        close(sock);
        return;
    }
    
    // Receive encrypted PDF
    ssize_t totalReceived = 0;
    while (totalReceived < pdfSize) {
        ssize_t bytesRead = read(sock, encryptedPdf + totalReceived, pdfSize - totalReceived);
        if (bytesRead <= 0) {
            perror("Read PDF data");
            free(encryptedPdf);
            close(sock);
            return;
        }
        totalReceived += bytesRead;
    }
    
    printf("[Client] Received encrypted PDF data (%zd bytes)\n", totalReceived);

    // Receive tag
    unsigned char tag[TAG_LEN] = {0};
    ssize_t tagBytes = read(sock, tag, TAG_LEN);
    if (tagBytes != TAG_LEN) {
        perror("Read tag failed");
        free(encryptedPdf);
        close(sock);
        return;
    }
    
    printf("[Client] Received authentication tag\n");

    // Allocate memory for decrypted PDF
    unsigned char *decryptedPdf = malloc(pdfSize);
    if (!decryptedPdf) {
        perror("Memory allocation failed");
        free(encryptedPdf);
        close(sock);
        return;
    }

    // Decrypt PDF
    int ret = decryptData(encryptedPdf, pdfSize, kap, nonce, decryptedPdf, tag);
    if (ret != 1) {
        fprintf(stderr, "Decryption failed: Invalid tag/corrupted data (return code: %d)\n", ret);
        free(encryptedPdf);
        free(decryptedPdf);
        close(sock);
        return;
    }
    
    printf("[Client] Decrypted PDF successfully\n");

    // Save decrypted PDF
    FILE *pdf = fopen("received.pdf", "wb");
    if (pdf == NULL) {
        perror("Failed to open output PDF");
        free(encryptedPdf);
        free(decryptedPdf);
        close(sock);
        return;
    }

    if (fwrite(decryptedPdf, 1, pdfSize, pdf) != pdfSize) {
        perror("Failed to write PDF file");
        fclose(pdf);
        free(encryptedPdf);
        free(decryptedPdf);
        close(sock);
        return;
    }
    
    fclose(pdf);
    free(encryptedPdf);
    free(decryptedPdf);
    close(sock);
    printf("[Client] PDF saved as 'received.pdf'\n");
    logMessage("PDF received and decrypted successfully");
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <filename> <server_ip>\n", argv[0]);
        return 1;
    }

    const char *filename = argv[1];
    const char *server_ip = argv[2];
    printf("[Client] Requesting conversion of file: %s\n", filename);

    // Connect to KDC
    int kdcSock = socket(AF_INET, SOCK_STREAM, 0);
    if (kdcSock < 0) {
        perror("Socket creation failed");
        return 1;
    }

    struct sockaddr_in kdcAddr = {
        .sin_family = AF_INET, 
        .sin_port = htons(KDC_PORT), 
        .sin_addr.s_addr = inet_addr(server_ip)
    };
    if (connect(kdcSock, (struct sockaddr *)&kdcAddr, sizeof(kdcAddr)) < 0) {
        perror("Connection to KDC failed");
        close(kdcSock);
        return 1;
    }
    
    printf("[Client] Connected to KDC\n");

    // Send username
    const char *username = "alice";
    if (write(kdcSock, username, strlen(username) + 1) <= 0) {
        perror("Write username failed");
        close(kdcSock);
        return 1;
    }
    
    printf("[Client] Sent username '%s' to KDC\n", username);

    // Derive client key
    unsigned char clientKey[KEY_LEN] = {0}, salt[SALT_LEN] = {0};
    memcpy(salt, KDC_SALT, SALT_LEN);
    deriveKey("alice_password", salt, clientKey);

    // Receive nonce from KDC
    unsigned char nonce[NONCE_LEN] = {0};
    ssize_t nonceBytes = read(kdcSock, nonce, NONCE_LEN);
    if (nonceBytes != NONCE_LEN) {
        perror("Read nonce failed");
        close(kdcSock);
        return 1;
    }
    
    printf("[Client] Received nonce from KDC\n");

    // Receive encrypted session key
    unsigned char encSessionKey[KEY_LEN] = {0};
    ssize_t keyBytes = read(kdcSock, encSessionKey, KEY_LEN);
    if (keyBytes != KEY_LEN) {
        perror("Read session key failed");
        close(kdcSock);
        return 1;
    }
    
    printf("[Client] Received encrypted session key from KDC\n");

    // Receive tag from KDC
    unsigned char tag[TAG_LEN] = {0};
    ssize_t tagBytes = read(kdcSock, tag, TAG_LEN);
    if (tagBytes != TAG_LEN) {
        perror("Read tag failed");
        close(kdcSock);
        return 1;
    }
    
    printf("[Client] Received authentication tag from KDC\n");

    // Decrypt session key
    unsigned char kap[KEY_LEN] = {0};
    int ret = decryptData(encSessionKey, KEY_LEN, clientKey, nonce, kap, tag);
    if (ret != 1) {
        fprintf(stderr, "Session key decryption failed: Invalid tag/corrupted data (return code: %d)\n", ret);
        close(kdcSock);
        return 1;
    }
    
    printf("[Client] Decrypted session key successfully\n");
    close(kdcSock);

    // Connect to Print Server using the session key
    connectToPrintServer(kap, nonce, filename, server_ip);

    return 0;
}