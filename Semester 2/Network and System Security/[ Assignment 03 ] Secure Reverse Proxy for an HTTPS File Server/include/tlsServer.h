#ifndef TLS_SERVER_H
#define TLS_SERVER_H

#include <openssl/ssl.h>

SSL_CTX* setupTlsServer(const char* certFile, const char* keyFile);
int setupServerSocket(int port);
int acceptClient(int serverFd);

#endif