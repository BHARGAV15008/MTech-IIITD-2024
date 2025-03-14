#ifndef CryptoUtilsH
#define CryptoUtilsH

#include <openssl/evp.h>
#include <openssl/rand.h>
#include <openssl/err.h>
#include "config.h"

void handleErrors();
void deriveKey(const char *passphrase, const unsigned char *salt, unsigned char *key);
void encryptData(unsigned char *plaintext, int plaintextLen,
                 unsigned char *key, unsigned char *nonce,
                 unsigned char *ciphertext, unsigned char *tag);
int decryptData(unsigned char *ciphertext, int ciphertextLen,
                unsigned char *key, unsigned char *nonce,
                unsigned char *plaintext, unsigned char *tag);
void generateNonce(unsigned char *nonce);

#endif