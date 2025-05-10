#include "utils.h"
#include <openssl/err.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void logError(const char* msg) {
    fprintf(stderr, "%s: ", msg);
    ERR_print_errors_fp(stderr);
}

int sendMessage(SSL* ssl, const char* msg) {
    return SSL_write(ssl, msg, strlen(msg));
}

int receiveMessage(SSL* ssl, char* buffer, int size) {
    int len = SSL_read(ssl, buffer, size - 1);
    if (len > 0) buffer[len] = '\0';
    return len;
}

void handleFileDownload(SSL* ssl, const char* response) {
    int size;
    sscanf(response, "OK %d", &size);
    char* content = malloc(size + 1);
    int received = 0;
    while (received < size) {
        int len = SSL_read(ssl, content + received, size - received);
        if (len <= 0) break;
        received += len;
    }
    content[received] = '\0';
    FILE* fp = fopen("downloaded_file", "wb");
    if (fp) {
        fwrite(content, 1, received, fp);
        fclose(fp);
    }
    free(content);
}