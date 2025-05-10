#ifndef CONFIG_H
#define CONFIG_H

#define KDC_PORT 5000
#define PRN_PORT 5001
#define MAX_CLIENTS 10
#define THREAD_POOL_SIZE 5
#define LOG_FILE "server.log"
#define KDC_SALT "fixed_salt_bhargav"
#define KEY_LEN 32                   // AES-256 key length
#define NONCE_LEN 12                 // GCM nonce length
#define TAG_LEN 16                   // GCM tag length
#define SALT_LEN 16                  // Salt length for key derivation

#endif