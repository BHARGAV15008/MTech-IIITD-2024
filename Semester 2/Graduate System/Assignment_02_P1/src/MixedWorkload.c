#define _GNU_SOURCE
#include "../include/MixedWorkload.h"
#include "../include/Common.h"
#include <fcntl.h>
#include <stdint.h>
#include <immintrin.h>
#include <libaio.h>
#include <string.h>

typedef struct {
    double* matrix;
    volatile uint64_t* data;
    int fileDesc;
    size_t size;
} MixedThreadData;

static void* mixedWorker(void* arg) {
    MixedThreadData* d = (MixedThreadData*)arg;
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    // CPU-bound (AVX2)
    for(size_t i = 0; i < d->size; i += 4) {
        __m256d vec = _mm256_load_pd(&d->matrix[i]);
        vec = _mm256_mul_pd(vec, vec);
        _mm256_store_pd(&d->matrix[i], vec);
    }

    // Memory-bound
    const size_t stride = sysconf(_SC_LEVEL1_DCACHE_LINESIZE);
    for(size_t i = 0; i < d->size; i += stride) {
        d->data[i] = d->data[i] * 3 + 1;
    }

    // I/O-bound
    io_context_t ctx = 0;
    struct iocb cb;
    struct iocb* cbs[1] = {&cb};
    
    if(io_setup(1, &ctx) == 0) {
        for(size_t offset = 0; offset < d->size; offset += 4096) {
            io_prep_pwrite(&cb, d->fileDesc, 
                          (void*)(d->data + offset), 
                          4096, offset);
            io_submit(ctx, 1, cbs);
            struct io_event ev;
            io_getevents(ctx, 1, 1, &ev, NULL);
        }
        io_destroy(ctx);
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    printTime("Mixed Thread", start, end);
    return NULL;
}

void runMixedWorkload(int threadCount) {
    pthread_t workers[threadCount];
    MixedThreadData threadData[threadCount];
    size_t size = 1UL << 24; // 16M elements

    struct timespec globalStart, globalEnd;
    clock_gettime(CLOCK_MONOTONIC, &globalStart);

    for(int i = 0; i < threadCount; i++) {
        posix_memalign((void**)&threadData[i].matrix, 64, size * sizeof(double));
        threadData[i].data = numa_alloc_local(size * sizeof(uint64_t));
        threadData[i].fileDesc = open("/tmp/mixedfile", 
                                    O_DIRECT | O_RDWR | O_CREAT, 
                                    0644);
        threadData[i].size = size;
        pthread_create(&workers[i], NULL, mixedWorker, &threadData[i]);
    }

    for(int i = 0; i < threadCount; i++) {
        pthread_join(workers[i], NULL);
        free(threadData[i].matrix);
        numa_free((void*)threadData[i].data, size * sizeof(uint64_t));
        close(threadData[i].fileDesc);
    }

    clock_gettime(CLOCK_MONOTONIC, &globalEnd);
    printTime("Total Mixed Workload", globalStart, globalEnd);
}