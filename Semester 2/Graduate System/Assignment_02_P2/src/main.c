#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "buffer.h"
#include "producer.h"
#include "consumer.h"
#include "utils.h"

#define DEFAULT_BUFFER_SIZE 10
#define DEFAULT_ITEMS_PER_PRODUCER 100

// Structure to hold performance metrics
typedef struct {
    double executionTime;        // Total execution time in seconds
    int totalItemsProcessed;     // Total items processed across all consumers
    double throughput;           // Items processed per second
    double* consumerAverages;    // Average value per consumer
} PerformanceMetrics;

// Function to run the producer-consumer test
PerformanceMetrics runProducerConsumerTest(int numPairs, int bufferSize, int itemsPerProducer) {
    PerformanceMetrics metrics = {0};
    Timer timer;

    // Allocate arrays for thread management
    pthread_t* producerThreads = malloc(numPairs * sizeof(pthread_t));
    pthread_t* consumerThreads = malloc(numPairs * sizeof(pthread_t));
    Buffer** buffers = malloc(numPairs * sizeof(Buffer*));
    ProducerArgs* producerArgs = malloc(numPairs * sizeof(ProducerArgs));
    ConsumerArgs* consumerArgs = malloc(numPairs * sizeof(ConsumerArgs));

    // Allocate arrays for results
    int* itemsProcessed = calloc(numPairs, sizeof(int));
    metrics.consumerAverages = calloc(numPairs, sizeof(double));

    // Initialize random number generator
    randomInit();

    // Start timing
    timerStart(&timer);

    // Create buffers and start threads
    for (int i = 0; i < numPairs; i++) {
        // Create buffer for this producer-consumer pair
        buffers[i] = bufferInit(bufferSize);
        if (!buffers[i]) {
            fprintf(stderr, "Error initializing buffer for pair %d\n", i);
            exit(EXIT_FAILURE);
        }

        // Set up producer arguments
        producerArgs[i].id = i;
        producerArgs[i].buffer = buffers[i];
        producerArgs[i].itemsToProduce = itemsPerProducer;

        // Set up consumer arguments
        consumerArgs[i].id = i;
        consumerArgs[i].buffer = buffers[i];
        consumerArgs[i].itemsProcessed = &itemsProcessed[i];
        consumerArgs[i].result = &metrics.consumerAverages[i];

        // Create threads
        pthread_create(&producerThreads[i], NULL, producerFunction, &producerArgs[i]);
        pthread_create(&consumerThreads[i], NULL, consumerFunction, &consumerArgs[i]);
    }

    // Wait for producer threads to finish
    for (int i = 0; i < numPairs; i++) {
        pthread_join(producerThreads[i], NULL);
        bufferSetDone(buffers[i]);  // Signal consumers that no more items will be produced
    }

    // Wait for consumer threads to finish
    for (int i = 0; i < numPairs; i++) {
        pthread_join(consumerThreads[i], NULL);
    }

    // Stop timing
    timerStop(&timer);

    // Calculate performance metrics
    metrics.executionTime = timerElapsedSeconds(&timer);
    metrics.totalItemsProcessed = 0;

    for (int i = 0; i < numPairs; i++) {
        metrics.totalItemsProcessed += itemsProcessed[i];
    }

    metrics.throughput = metrics.totalItemsProcessed / metrics.executionTime;

    // Clean up
    for (int i = 0; i < numPairs; i++) {
        bufferDestroy(buffers[i]);
    }

    free(producerThreads);
    free(consumerThreads);
    free(buffers);
    free(producerArgs);
    free(consumerArgs);
    free(itemsProcessed);

    return metrics;
}

// Function to print usage information
void printUsage(const char* programName) {
    printf("Usage: %s [numPairs] [bufferSize] [itemsPerProducer]\n", programName);
    printf("  numPairs:           Number of producer-consumer thread pairs (default: 4)\n");
    printf("  bufferSize:         Size of each shared buffer (default: %d)\n", DEFAULT_BUFFER_SIZE);
    printf("  itemsPerProducer:  Number of items each producer generates (default: %d)\n", DEFAULT_ITEMS_PER_PRODUCER);
}

int main(int argc, char* argv[]) {
    int numPairs = 4;  // Default number of producer-consumer pairs
    int bufferSize = DEFAULT_BUFFER_SIZE;
    int itemsPerProducer = DEFAULT_ITEMS_PER_PRODUCER;

    // Parse command-line arguments
    if (argc > 1) {
        numPairs = atoi(argv[1]);
        if (numPairs <= 0) {
            fprintf(stderr, "Error: Number of thread pairs must be positive\n");
            printUsage(argv[0]);
            return 1;
        }
    }

    if (argc > 2) {
        bufferSize = atoi(argv[2]);
        if (bufferSize <= 0) {
            fprintf(stderr, "Error: Buffer size must be positive\n");
            printUsage(argv[0]);
            return 1;
        }
    }

    if (argc > 3) {
        itemsPerProducer = atoi(argv[3]);
        if (itemsPerProducer <= 0) {
            fprintf(stderr, "Error: Items per producer must be positive\n");
            printUsage(argv[0]);
            return 1;
        }
    }

    // Print configuration
    printf("Running producer-consumer test with:\n");
    printf("  Thread pairs:        %d\n", numPairs);
    printf("  Buffer size:         %d\n", bufferSize);
    printf("  Items per producer:  %d\n", itemsPerProducer);
    printf("  Total items:         %d\n", numPairs * itemsPerProducer);
    printf("\n");

    // Run the test
    PerformanceMetrics metrics = runProducerConsumerTest(numPairs, bufferSize, itemsPerProducer);

    // Print performance results
    printf("\nPerformance Results:\n");
    printf("  Execution time:       %.4f seconds\n", metrics.executionTime);
    printf("  Total items processed: %d\n", metrics.totalItemsProcessed);
    printf("  Throughput:           %.2f items/second\n", metrics.throughput);
    printf("\n");

    printf("Consumer Results:\n");
    for (int i = 0; i < numPairs; i++) {
        printf("  Consumer %d average: %.2f\n", i, metrics.consumerAverages[i]);
    }

    // Clean up
    free(metrics.consumerAverages);

    return 0;
}