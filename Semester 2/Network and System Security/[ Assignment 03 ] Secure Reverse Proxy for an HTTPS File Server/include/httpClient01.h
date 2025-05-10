#ifndef HTTP_CLIENT_H
#define HTTP_CLIENT_H
#include <openssl/ssl.h>
void listFiles(SSL* clientSsl);
void getFile(SSL* clientSsl, const char* filename);
void putFile(SSL* clientSsl, const char* filename, int size);
#endif