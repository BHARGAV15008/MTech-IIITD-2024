#include "tlsClient.h"
#include <openssl/err.h>
#include <openssl/x509v3.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include "utils.h"

int customVerifyCallback(int preverify_ok, X509_STORE_CTX* ctx) {
    if (!preverify_ok) {
        X509* cert = X509_STORE_CTX_get_current_cert(ctx);
        int err = X509_STORE_CTX_get_error(ctx);
        char buf[256];
        X509_NAME_oneline(X509_get_subject_name(cert), buf, sizeof(buf));
        fprintf(stderr, "Certificate verification failed: %s (%s)\n", 
                X509_verify_cert_error_string(err), buf);
        return 0;
    }

    X509* cert = X509_STORE_CTX_get_current_cert(ctx);
    time_t now = time(NULL);
    if (X509_cmp_time(X509_get_notBefore(cert), &now) > 0 ||
        X509_cmp_time(X509_get_notAfter(cert), &now) < 0) {
        fprintf(stderr, "Certificate expired or not yet valid\n");
        return 0;
    }

    return 1;
}

SSL_CTX* setupTlsClient(const char* caFile, int (*verifyCallback)(int, X509_STORE_CTX*)) {
    SSL_library_init();
    OpenSSL_add_all_algorithms();
    SSL_load_error_strings();

    SSL_CTX* ctx = SSL_CTX_new(TLS_client_method());
    if (!ctx) {
        logError("Failed to create TLS context");
        return NULL;
    }

    if (SSL_CTX_load_verify_locations(ctx, caFile, NULL) <= 0) {
        logError("Failed to load CA certificate");
        SSL_CTX_free(ctx);
        return NULL;
    }

    SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER, verifyCallback ? verifyCallback : customVerifyCallback);
    SSL_CTX_set_verify_depth(ctx, 4);
    return ctx;
}

int connectToServer(const char* host, int port) {
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0) {
        logError("Failed to create socket");
        return -1;
    }

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    if (inet_pton(AF_INET, host, &addr.sin_addr) <= 0) {
        logError("Invalid address");
        close(sock);
        return -1;
    }

    if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        logError("Failed to connect to server");
        close(sock);
        return -1;
    }
    return sock;
}