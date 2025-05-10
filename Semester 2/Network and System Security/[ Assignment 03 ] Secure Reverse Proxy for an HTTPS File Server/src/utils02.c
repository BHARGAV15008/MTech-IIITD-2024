#include "utils.h"
#include <openssl/err.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void logError(const char* msg) {
    fprintf(stderr, "%s: ", msg);
    unsigned long err;
    while ((err = ERR_get_error())) {
        char buf[256];
        ERR_error_string_n(err, buf, sizeof(buf));
        fprintf(stderr, "%s\n", buf);
    }
}

int sendMessage(SSL* ssl, const char* msg) {
    int len = strlen(msg);
    int written = SSL_write(ssl, msg, len);
    if (written <= 0) {
        logError("Failed to send message");
    }
    return written;
}

int receiveMessage(SSL* ssl, char* buffer, int size) {
    int len = SSL_read(ssl, buffer, size - 1);
    if (len > 0) {
        buffer[len] = '\0';
    } else if (len <= 0) {
        logError("Failed to receive message");
    }
    return len;
}

void handleFileDownload(SSL* ssl, const char* response, const char* filename) {
    int size;
    if (sscanf(response, "OK %d", &size) != 1) {
        fprintf(stderr, "ERROR: Invalid response format\n");
        return;
    }
    char* content = malloc(size + 1);
    if (!content) {
        fprintf(stderr, "ERROR: Memory allocation failed\n");
        return;
    }
    int received = 0;
    while (received < size) {
        int len = SSL_read(ssl, content + received, size - received);
        if (len <= 0) {
            fprintf(stderr, "ERROR: Failed to receive file content\n");
            break;
        }
        received += len;
    }
    content[received] = '\0';
    FILE* fp = fopen(filename, "wb");
    if (fp) {
        fwrite(content, 1, received, fp);
        fclose(fp);
    } else {
        fprintf(stderr, "ERROR: Failed to open file %s\n", filename);
    }
    free(content);
}