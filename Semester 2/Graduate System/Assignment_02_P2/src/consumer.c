#include "consumer.h"
#include <stdio.h>

// Function for consumer threads
void* consumerFunction(void* arg) {
    ConsumerArgs* args = (ConsumerArgs*)arg;
    int item;
    int count = 0;
    double sum = 0.0;

    // Process items from the buffer until done
    while (1) {
        // Get an item from the buffer
        item = bufferGet(args->buffer);

        // Check if we're done
        if (item == -1) {
            break; // Exit loop if no more items
        }

        // Process the item (calculate running average)
        count++;
        sum += item;

        // Optional: Print status (can be removed for performance testing)
        printf("Consumer %d: Consumed item %d, Running avg: %.2f\n", 
               args->id, item, sum / count);
    }

    // Store results
    if (args->itemsProcessed) {
        *(args->itemsProcessed) = count; // Store number of items processed
    }

    if (args->result) {
        *(args->result) = count > 0 ? sum / count : 0.0; // Calculate average
    }

    printf("Consumer %d: Finished consuming %d items, Average: %.2f\n", 
           args->id, count, count > 0 ? sum / count : 0.0);

    return NULL;
}