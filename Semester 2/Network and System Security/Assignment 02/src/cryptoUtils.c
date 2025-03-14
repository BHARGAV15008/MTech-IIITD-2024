#include "cryptoUtils.h"
#include <string.h>

void handleErrors() {
    ERR_print_errors_fp(stderr);
    abort();
}

void deriveKey(const char *passphrase, const unsigned char *salt, unsigned char *key) {
    if (PKCS5_PBKDF2_HMAC(passphrase, strlen(passphrase), salt, SALT_LEN, 100000,
                          EVP_sha256(), KEY_LEN, key) != 1) {
        handleErrors();
    }
}

void encryptData(unsigned char *plaintext, int plaintextLen,
                  unsigned char *key, unsigned char *nonce,
                  unsigned char *ciphertext, unsigned char *tag) {
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (!ctx) handleErrors();

    if (EVP_EncryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, NULL, NULL) != 1) handleErrors();
    if (EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, NONCE_LEN, NULL) != 1) handleErrors();
    if (EVP_EncryptInit_ex(ctx, NULL, NULL, key, nonce) != 1) handleErrors();

    int len;
    if (EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintextLen) != 1) handleErrors();
    if (EVP_EncryptFinal_ex(ctx, ciphertext + len, &len) != 1) handleErrors();

    if (EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG, TAG_LEN, tag) != 1) handleErrors();
    EVP_CIPHER_CTX_free(ctx);
}

int decryptData(unsigned char *ciphertext, int ciphertextLen,
                 unsigned char *key, unsigned char *nonce,
                 unsigned char *plaintext, unsigned char *tag) {
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (!ctx) handleErrors();

    if (EVP_DecryptInit_ex(ctx, EVP_aes_256_gcm(), NULL, NULL, NULL) != 1) handleErrors();
    if (EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_IVLEN, NONCE_LEN, NULL) != 1) handleErrors();
    if (EVP_DecryptInit_ex(ctx, NULL, NULL, key, nonce) != 1) handleErrors();

    int len, ret;
    if (EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, ciphertextLen) != 1) handleErrors();
    if (EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_TAG, TAG_LEN, tag) != 1) handleErrors();
    ret = EVP_DecryptFinal_ex(ctx, plaintext + len, &len);

    EVP_CIPHER_CTX_free(ctx);
    return ret;
}

void generateNonce(unsigned char *nonce) {
    if (RAND_bytes(nonce, NONCE_LEN) != 1) handleErrors();
}