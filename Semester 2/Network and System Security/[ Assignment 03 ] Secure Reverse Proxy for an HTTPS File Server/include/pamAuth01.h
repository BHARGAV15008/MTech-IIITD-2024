#ifndef PAM_AUTH_H
#define PAM_AUTH_H
#include <openssl/ssl.h>
int authenticateUser(const char* username, const char* password);
int handleLogin(SSL* ssl);
#endif