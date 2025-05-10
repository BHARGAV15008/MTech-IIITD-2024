#include "httpClient.h"
#include "tlsClient.h"
#include "utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void listFiles(SSL* clientSsl) {
    SSL_CTX* ctx = setupTlsClient("certs/ca.crt");
    if (!ctx) {
        sendMessage(clientSsl, "ERROR Failed to setup TLS client\n");
        return;
    }

    int sock = connectToServer("localhost", 443);
    if (sock < 0) {
        sendMessage(clientSsl, "ERROR Server connection failed\n");
        SSL_CTX_free(ctx);
        return;
    }

    SSL* ssl = SSL_new(ctx);
    SSL_set_fd(ssl, sock);
    if (SSL_connect(ssl) <= 0) {
        sendMessage(clientSsl, "ERROR Server connection failed\n");
        goto cleanup;
    }

    char request[256];
    snprintf(request, sizeof(request), "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n");
    SSL_write(ssl, request, strlen(request));

    char buffer[4096] = {0};
    int len = SSL_read(ssl, buffer, sizeof(buffer) - 1);
    if (len <= 0) {
        sendMessage(clientSsl, "ERROR Failed to read server response\n");
        goto cleanup;
    }
    buffer[len] = '\0';

    char* pos = buffer;
    while ((pos = strstr(pos, "<a href=\"")) != NULL) {
        pos += 9;
        char* end = strchr(pos, '"');
        if (!end) break;
        *end = '\0';
        if (strcmp(pos, ".") != 0 && strcmp(pos, "..") != 0 && pos[0] != '/') {
            sendMessage(clientSsl, pos);
            sendMessage(clientSsl, "\n");
        }
        pos = end + 1;
    }
    sendMessage(clientSsl, "END\n");

cleanup:
    SSL_shutdown(ssl);
    SSL_free(ssl);
    close(sock);
    SSL_CTX_free(ctx);
}

void getFile(SSL* clientSsl, const char* filename) {
    SSL_CTX* ctx = setupTlsClient("certs/ca.crt");
    if (!ctx) {
        sendMessage(clientSsl, "ERROR Failed to setup TLS client\n");
        return;
    }

    int sock = connectToServer("localhost", 443);
    if (sock < 0) {
        sendMessage(clientSsl, "ERROR Server connection failed\n");
        SSL_CTX_free(ctx);
        return;
    }

    SSL* ssl = SSL_new(ctx);
    SSL_set_fd(ssl, sock);
    if (SSL_connect(ssl) <= 0) {
        sendMessage(clientSsl, "ERROR Server connection failed\n");
        goto cleanup;
    }

    char request[256];
    snprintf(request, sizeof(request), "GET /%s HTTP/1.1\r\nHost: localhost\r\n\r\n", filename);
    SSL_write(ssl, request, strlen(request));

    char buffer[4096];
    int len = SSL_read(ssl, buffer, sizeof(buffer) - 1);
    buffer[len] = '\0';

    char* body = strstr(buffer, "\r\n\r\n");
    if (!body) {
        sendMessage(clientSsl, "ERROR File not found\n");
    } else {
        body += 4;
        int size = len - (body - buffer);
        char response[256];
        snprintf(response, sizeof(response), "OK %d\n", size);
        sendMessage(clientSsl, response);
        SSL_write(clientSsl, body, size);
    }

cleanup:
    SSL_shutdown(ssl);
    SSL_free(ssl);
    close(sock);
    SSL_CTX_free(ctx);
}

void putFile(SSL* clientSsl, const char* filename, int size) {
    char* content = malloc(size);
    int received = 0;
    while (received < size) {
        int len = SSL_read(clientSsl, content + received, size - received);
        if (len <= 0) {
            fprintf(stderr, "putFile: Failed to read %d bytes, received %d\n", size, received);
            sendMessage(clientSsl, "ERROR File upload failed\n");
            free(content);
            return;
        }
        received += len;
    }
    content[size] = '\0';

    SSL_CTX* ctx = setupTlsClient("certs/ca.crt");
    if (!ctx) {
        sendMessage(clientSsl, "ERROR Failed to setup TLS client\n");
        free(content);
        return;
    }

    int sock = connectToServer("localhost", 443);
    if (sock < 0) {
        sendMessage(clientSsl, "ERROR Server connection failed\n");
        free(content);
        SSL_CTX_free(ctx);
        return;
    }

    SSL* ssl = SSL_new(ctx);
    SSL_set_fd(ssl, sock);
    if (SSL_connect(ssl) <= 0) {
        fprintf(stderr, "putFile: Failed to connect to Nginx\n");
        sendMessage(clientSsl, "ERROR Server connection failed\n");
        goto cleanup;
    }

    char request[512];
    snprintf(request, sizeof(request),
             "PUT /%s HTTP/1.1\r\nHost: localhost\r\nContent-Length: %d\r\n\r\n",
             filename, size);
    SSL_write(ssl, request, strlen(request));
    SSL_write(ssl, content, size);

    char buffer[256];
    int len = SSL_read(ssl, buffer, sizeof(buffer) - 1);
    buffer[len] = '\0';
    if (strstr(buffer, "201") || strstr(buffer, "200")) {
        sendMessage(clientSsl, "OK\n");
    } else {
        fprintf(stderr, "putFile: Nginx response: %s\n", buffer);
        sendMessage(clientSsl, "ERROR Upload failed\n");
    }

cleanup:
    free(content);
    SSL_shutdown(ssl);
    SSL_free(ssl);
    close(sock);
    SSL_CTX_free(ctx);
}
