#include "tlsServer.h"
#include <openssl/err.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <stdio.h>
#include "utils.h"

SSL_CTX* setupTlsServer(const char* certFile, const char* keyFile) {
    SSL_library_init();
    OpenSSL_add_all_algorithms();
    SSL_load_error_strings();

    SSL_CTX* ctx = SSL_CTX_new(TLS_server_method());
    if (!ctx) {
        logError("Failed to create TLS context");
        return NULL;
    }

    if (SSL_CTX_use_certificate_file(ctx, certFile, SSL_FILETYPE_PEM) <= 0 ||
        SSL_CTX_use_PrivateKey_file(ctx, keyFile, SSL_FILETYPE_PEM) <= 0) {
        logError("Failed to load certificate or key");
        SSL_CTX_free(ctx);
        return NULL;
    }

    if (!SSL_CTX_check_private_key(ctx)) {
        logError("Private key does not match certificate");
        SSL_CTX_free(ctx);
        return NULL;
    }

    return ctx;
}

int setupServerSocket(int port) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        logError("Failed to create socket");
        return -1;
    }

    int opt = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt)) < 0) {
        logError("Failed to set socket options");
        close(sock);
        return -1;
    }

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = INADDR_ANY;
    addr.sin_port = htons(port);

    if (bind(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0 ||
        listen(sock, 10) < 0) {
        logError("Failed to bind or listen");
        close(sock);
        return -1;
    }
    return sock;
}

int acceptClient(int serverFd) {
    struct sockaddr_in clientAddr;
    socklen_t len = sizeof(clientAddr);
    int clientFd = accept(serverFd, (struct sockaddr*)&clientAddr, &len);
    if (clientFd < 0) {
        logError("Failed to accept client");
    }
    return clientFd;
}