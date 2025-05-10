#ifndef TLS_CLIENT_H
#define TLS_CLIENT_H
#include <openssl/ssl.h>
SSL_CTX* setupTlsClient(const char* caFile, int (*verifyCallback)(int, X509_STORE_CTX*));
int connectToServer(const char* host, int port);
#endif