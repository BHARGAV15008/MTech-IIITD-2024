#include "../include/MemWorkload.h"
#include "../include/Common.h"
#include <stdint.h>  // Add this for uint64_t
#include <numa.h>

typedef struct {
    volatile uint64_t* data;
    size_t size;
    int numaNode;
} MemThreadData;

static void* memoryWorker(void* arg) {
    MemThreadData* d = (MemThreadData*)arg;
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    const size_t stride = sysconf(_SC_LEVEL1_DCACHE_LINESIZE);
    for(size_t i = 0; i < d->size; i += stride) {
        d->data[i] = d->data[i] * 3 + 1;
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    printTime("Memory Thread", start, end);
    return NULL;
}

void runMemWorkload(int threadCount) {
    pthread_t workers[threadCount];
    MemThreadData threadData[threadCount];
    size_t size = 1UL << 30; // 1GB
    volatile uint64_t* sharedData = numa_alloc_interleaved(size);

    struct timespec globalStart, globalEnd;
    clock_gettime(CLOCK_MONOTONIC, &globalStart);

    for(int i = 0; i < threadCount; i++) {
        threadData[i].data = sharedData + (i * (size/threadCount));
        threadData[i].size = size/threadCount;
        threadData[i].numaNode = i % numa_max_node();
        pthread_create(&workers[i], NULL, memoryWorker, &threadData[i]);
    }

    for(int i = 0; i < threadCount; i++) {
        pthread_join(workers[i], NULL);
    }

    clock_gettime(CLOCK_MONOTONIC, &globalEnd);
    printTime("Total Memory Workload", globalStart, globalEnd);
    numa_free((void*)sharedData, size);
}