#ifndef UTILS_H
#define UTILS_H

#include <openssl/ssl.h>

void logError(const char* msg);
int sendMessage(SSL* ssl, const char* msg);
int receiveMessage(SSL* ssl, char* buffer, int size);
void handleFileDownload(SSL* ssl, const char* response);

#endif