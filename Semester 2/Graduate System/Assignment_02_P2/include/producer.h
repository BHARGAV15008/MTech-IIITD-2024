#ifndef PRODUCER_H
#define PRODUCER_H

#include "buffer.h"

// Producer thread arguments
typedef struct {
    int id;                   // Producer identifier
    Buffer* buffer;           // Shared buffer
    int itemsToProduce;       // Number of items to produce
} ProducerArgs;

// Producer function
void* producerFunction(void* arg);

#endif // PRODUCER_H