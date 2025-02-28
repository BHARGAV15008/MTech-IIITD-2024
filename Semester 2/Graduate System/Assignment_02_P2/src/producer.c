#include "producer.h"
#include "utils.h"
#include <stdio.h>
#include <stdlib.h>

// Function for producer threads
void* producerFunction(void* arg) {
    ProducerArgs* args = (ProducerArgs*)arg;

    // Generate and put items into the buffer
    for (int i = 0; i < args->itemsToProduce; i++) {
        // Generate a random value between 1 and 100
        int value = randomRange(1, 100);

        // Put the value into the buffer
        bufferPut(args->buffer, value);

        // Optional: Print status (can be removed for performance testing)
        printf("Producer %d: Produced item %d\n", args->id, value);
    }

    printf("Producer %d: Finished producing %d items\n", 
           args->id, args->itemsToProduce);

    return NULL;
}