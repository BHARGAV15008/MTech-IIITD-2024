#ifndef BUFFER_H
#define BUFFER_H

#include <pthread.h>
#include <stdbool.h>

// Buffer structure to hold shared data between producer and consumer
typedef struct {
    int* data;                // Array to store items
    int capacity;             // Maximum buffer capacity
    int count;                // Current number of items in buffer
    int inIndex;              // Index for next insertion
    int outIndex;             // Index for next removal
    pthread_mutex_t bufferMutex;  // Mutex for thread synchronization
    pthread_cond_t fullCond;      // Condition variable for buffer full
    pthread_cond_t emptyCond;     // Condition variable for buffer empty
    bool isDone;              // Flag to signal completion
} Buffer;

// Buffer operations
Buffer* bufferInit(int capacity);
void bufferDestroy(Buffer* buffer);
void bufferPut(Buffer* buffer, int item);
int bufferGet(Buffer* buffer);
void bufferSetDone(Buffer* buffer);
bool bufferIsDone(Buffer* buffer);

#endif // BUFFER_H