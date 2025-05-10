#include "httpClient.h"
#include "tlsClient.h"
#include "utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void listFiles(SSL* clientSsl) {
    SSL_CTX* ctx = setupTlsClient("certs/ca.crt", NULL);
    if (!ctx) {
        sendMessage(clientSsl, "ERROR: TLS setup failed\n");
        return;
    }

    int sock = connectToServer("localhost", 443);
    if (sock < 0) {
        sendMessage(clientSsl, "ERROR: Server connection failed\n");
        SSL_CTX_free(ctx);
        return;
    }

    SSL* ssl = SSL_new(ctx);
    if (!ssl) {
        sendMessage(clientSsl, "ERROR: Failed to create SSL object\n");
        close(sock);
        SSL_CTX_free(ctx);
        return;
    }
    SSL_set_fd(ssl, sock);

    if (SSL_connect(ssl) <= 0) {
        sendMessage(clientSsl, "ERROR: TLS handshake with server failed\n");
        goto cleanup;
    }

    char request[256];
    snprintf(request, sizeof(request), "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n");
    if (SSL_write(ssl, request, strlen(request)) <= 0) {
        sendMessage(clientSsl, "ERROR: Failed to send HTTP request\n");
        goto cleanup;
    }

    char* buffer = NULL;
    int total = 0, len;
    char temp[4096];
    while ((len = SSL_read(ssl, temp, sizeof(temp) - 1)) > 0) {
        buffer = realloc(buffer, total + len + 1);
        if (!buffer) {
            sendMessage(clientSsl, "ERROR: Memory allocation failed\n");
            goto cleanup;
        }
        memcpy(buffer + total, temp, len);
        total += len;
    }
    if (total == 0) {
        sendMessage(clientSsl, "ERROR: Failed to read server response\n");
        free(buffer);
        goto cleanup;
    }
    buffer[total] = '\0';

    char* pos = buffer;
    while ((pos = strstr(pos, "<a href=\"")) != NULL) {
        pos += 9;
        char* end = strchr(pos, '"');
        if (!end) break;
        *end = '\0';
        if (strcmp(pos, ".") != 0 && strcmp(pos, "..") != 0 && pos[0] != '/' && pos[0] != '\0') {
            sendMessage(clientSsl, pos);
            sendMessage(clientSsl, "\n");
        }
        pos = end + 1;
    }
    sendMessage(clientSsl, "END\n");
    free(buffer);

cleanup:
    if (ssl) {
        SSL_shutdown(ssl);
        SSL_free(ssl);
    }
    if (sock >= 0) close(sock);
    SSL_CTX_free(ctx);
}

void getFile(SSL* clientSsl, const char* filename) {
    SSL_CTX* ctx = setupTlsClient("certs/ca.crt", NULL);
    if (!ctx) {
        sendMessage(clientSsl, "ERROR: TLS setup failed\n");
        return;
    }

    int sock = connectToServer("localhost", 443);
    if (sock < 0) {
        sendMessage(clientSsl, "ERROR: Server connection failed\n");
        SSL_CTX_free(ctx);
        return;
    }

    SSL* ssl = SSL_new(ctx);
    if (!ssl) {
        sendMessage(clientSsl, "ERROR: Failed to create SSL object\n");
        close(sock);
        SSL_CTX_free(ctx);
        return;
    }
    SSL_set_fd(ssl, sock);

    if (SSL_connect(ssl) <= 0) {
        sendMessage(clientSsl, "ERROR: TLS handshake with server failed\n");
        goto cleanup;
    }

    char request[256];
    snprintf(request, sizeof(request), "GET /%s HTTP/1.1\r\nHost: localhost\r\n\r\n", filename);
    if (SSL_write(ssl, request, strlen(request)) <= 0) {
        sendMessage(clientSsl, "ERROR: Failed to send HTTP request\n");
        goto cleanup;
    }

    char* buffer = NULL;
    int total = 0, len;
    char temp[4096];
    while ((len = SSL_read(ssl, temp, sizeof(temp))) > 0) {
        buffer = realloc(buffer, total + len + 1);
        if (!buffer) {
            sendMessage(clientSsl, "ERROR: Memory allocation failed\n");
            goto cleanup;
        }
        memcpy(buffer + total, temp, len);
        total += len;
    }
    buffer[total] = '\0';

    char* content = strstr(buffer, "\r\n\r\n");
    if (!content || strstr(buffer, "404")) {
        sendMessage(clientSsl, "ERROR: File not found\n");
    } else {
        content += 4;
        int size = total - (content - buffer);
        char response[256];
        snprintf(response, sizeof(response), "OK %d\n", size);
        sendMessage(clientSsl, response);
        if (SSL_write(clientSsl, content, size) <= 0) {
            sendMessage(clientSsl, "ERROR: Failed to send file content\n");
        }
    }
    free(buffer);

cleanup:
    if (ssl) {
        SSL_shutdown(ssl);
        SSL_free(ssl);
    }
    if (sock >= 0) close(sock);
    SSL_CTX_free(ctx);
}

void putFile(SSL* clientSsl, const char* filename, int size) {
    char* content = malloc(size + 1);
    if (!content) {
        sendMessage(clientSsl, "ERROR: Memory allocation failed\n");
        return;
    }
    int received = 0;
    while (received < size) {
        int len = SSL_read(clientSsl, content + received, size - received);
        if (len <= 0) {
            sendMessage(clientSsl, "ERROR: File upload failed\n");
            free(content);
            return;
        }
        received += len;
    }
    content[size] = '\0';

    SSL_CTX* ctx = setupTlsClient("certs/ca.crt", NULL);
    if (!ctx) {
        sendMessage(clientSsl, "ERROR: TLS setup failed\n");
        free(content);
        return;
    }

    int sock = connectToServer("localhost", 443);
    if (sock < 0) {
        sendMessage(clientSsl, "ERROR: Server connection failed\n");
        free(content);
        SSL_CTX_free(ctx);
        return;
    }

    SSL* ssl = SSL_new(ctx);
    if (!ssl) {
        sendMessage(clientSsl, "ERROR: Failed to create SSL object\n");
        free(content);
        close(sock);
        SSL_CTX_free(ctx);
        return;
    }
    SSL_set_fd(ssl, sock);

    if (SSL_connect(素晴) <= 0) {
        sendMessage(clientSsl, "ERROR: TLS handshake with server failed\n");
        goto cleanup;
    }

    char request[512];
    snprintf(request, sizeof(request),
             "PUT /%s HTTP/1.1\r\nHost: localhost\r\nContent-Length: %d\r\n\r\n",
             filename, size);
    if (SSL_write(ssl, request, strlen(request)) <= 0 ||
        SSL_write(ssl, content, size) <= 0) {
        sendMessage(clientSsl, "ERROR: Failed to send HTTP request or content\n");
        goto cleanup;
    }

    char buffer[256];
    int len = SSL_read(ssl, buffer, sizeof(buffer) - 1);
    if (len <= 0) {
        sendMessage(clientSsl, "ERROR: Failed to read server response\n");
        goto cleanup;
    }
    buffer[len] = '\0';
    if (strstr(buffer, "201") || strstr(buffer, "200")) {
        sendMessage(clientSsl, "OK: File uploaded successfully\n");
    } else {
        sendMessage(clientSsl, "ERROR: Upload failed\n");
    }

cleanup:
    free(content);
    if (ssl) {
        SSL_shutdown(ssl);
        SSL_free(ssl);
    }
    if (sock >= 0) close(sock);
    SSL_CTX_free(ctx);
}