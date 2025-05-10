#ifndef PAM_AUTH_H
#define PAM_AUTH_H

#include <openssl/ssl.h>

int handleLogin(SSL* ssl);

#endif