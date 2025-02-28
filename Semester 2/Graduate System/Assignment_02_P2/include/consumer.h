#ifndef CONSUMER_H
#define CONSUMER_H

#include "buffer.h"

// Consumer thread arguments
typedef struct {
    int id;                   // Consumer identifier
    Buffer* buffer;           // Shared buffer
    int* itemsProcessed;      // Counter for processed items
    double* result;           // Result of processing (e.g., average)
} ConsumerArgs;

// Consumer function
void* consumerFunction(void* arg);

#endif // CONSUMER_H