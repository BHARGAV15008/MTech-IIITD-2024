#include "buffer.h"
#include <stdlib.h>
#include <stdio.h>

// Initialize the buffer with a given capacity
Buffer* bufferInit(int capacity) {
    Buffer* buffer = (Buffer*)malloc(sizeof(Buffer));
    if (!buffer) {
        perror("Failed to allocate buffer");
        return NULL;
    }

    // Allocate data array for the buffer
    buffer->data = (int*)malloc(capacity * sizeof(int));
    if (!buffer->data) {
        perror("Failed to allocate buffer data");
        free(buffer);
        return NULL;
    }

    // Initialize buffer state
    buffer->capacity = capacity;
    buffer->count = 0;
    buffer->inIndex = 0;
    buffer->outIndex = 0;
    buffer->isDone = false;

    // Initialize synchronization primitives
    pthread_mutex_init(&buffer->bufferMutex, NULL);
    pthread_cond_init(&buffer->fullCond, NULL);
    pthread_cond_init(&buffer->emptyCond, NULL);

    return buffer;
}

// Clean up the buffer and free resources
void bufferDestroy(Buffer* buffer) {
    if (!buffer) return;

    // Clean up synchronization primitives
    pthread_mutex_destroy(&buffer->bufferMutex);
    pthread_cond_destroy(&buffer->fullCond);
    pthread_cond_destroy(&buffer->emptyCond);

    // Free memory allocated for data
    free(buffer->data);
    free(buffer);
}

// Add an item to the buffer
void bufferPut(Buffer* buffer, int item) {
    pthread_mutex_lock(&buffer->bufferMutex); // Lock the mutex

    // Wait until there is space in the buffer
    while (buffer->count == buffer->capacity) {
        pthread_cond_wait(&buffer->fullCond, &buffer->bufferMutex);
    }

    // Add the item to the buffer
    buffer->data[buffer->inIndex] = item;
    buffer->inIndex = (buffer->inIndex + 1) % buffer->capacity; // Circular buffer
    buffer->count++;

    // Signal that the buffer is not empty
    pthread_cond_signal(&buffer->emptyCond);
    pthread_mutex_unlock(&buffer->bufferMutex); // Unlock the mutex
}

// Retrieve an item from the buffer
int bufferGet(Buffer* buffer) {
    int item;

    pthread_mutex_lock(&buffer->bufferMutex); // Lock the mutex

    // Wait until there is data or the producer is done
    while (buffer->count == 0 && !buffer->isDone) {
        pthread_cond_wait(&buffer->emptyCond, &buffer->bufferMutex);
    }

    // Check if we're done and there's nothing left to consume
    if (buffer->count == 0 && buffer->isDone) {
        pthread_mutex_unlock(&buffer->bufferMutex);
        return -1;  // Special value indicating end of stream
    }

    // Get the item from the buffer
    item = buffer->data[buffer->outIndex];
    buffer->outIndex = (buffer->outIndex + 1) % buffer->capacity; // Circular buffer
    buffer->count--;

    // Signal that the buffer is not full
    pthread_cond_signal(&buffer->fullCond);
    pthread_mutex_unlock(&buffer->bufferMutex); // Unlock the mutex

    return item;
}

// Signal that no more items will be produced
void bufferSetDone(Buffer* buffer) {
    pthread_mutex_lock(&buffer->bufferMutex);
    buffer->isDone = true;
    pthread_cond_broadcast(&buffer->emptyCond);  // Wake up all waiting consumers
    pthread_mutex_unlock(&buffer->bufferMutex);
}

// Check if the buffer is done processing
bool bufferIsDone(Buffer* buffer) {
    bool isDone;
    pthread_mutex_lock(&buffer->bufferMutex);
    isDone = buffer->isDone && (buffer->count == 0);
    pthread_mutex_unlock(&buffer->bufferMutex);
    return isDone;
}