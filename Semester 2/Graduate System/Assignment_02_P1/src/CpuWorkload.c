#include "../include/CpuWorkload.h"
#include "../include/Common.h"
#include <immintrin.h>

typedef struct {
    double* matrix;
    size_t size;
    int iterations;
} ThreadData;

static void* matrixWorker(void* arg) {
    ThreadData* data = (ThreadData*)arg;
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for(int i = 0; i < data->iterations; i++) {
        // Proper loop structure inside the function
        #pragma omp simd
        for(size_t j = 0; j < data->size; j += 4) {  // AVX2 compatible (256-bit)
            __m256d vec = _mm256_load_pd(&data->matrix[j]);
            vec = _mm256_mul_pd(vec, vec);
            _mm256_store_pd(&data->matrix[j], vec);
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    printTime("CPU Thread", start, end);
    return NULL;
}

void runCpuWorkload(int threadCount) {
    pthread_t workers[threadCount];
    ThreadData threadData[threadCount];
    size_t size = 1UL << 24; // 16M elements

    struct timespec globalStart, globalEnd;
    clock_gettime(CLOCK_MONOTONIC, &globalStart);

    for(int i = 0; i < threadCount; i++) {
        posix_memalign((void**)&threadData[i].matrix, 64, size * sizeof(double));
        threadData[i].size = size;
        threadData[i].iterations = 100;
        pthread_create(&workers[i], NULL, matrixWorker, &threadData[i]);
    }

    for(int i = 0; i < threadCount; i++) {
        pthread_join(workers[i], NULL);
        free(threadData[i].matrix);
    }

    clock_gettime(CLOCK_MONOTONIC, &globalEnd);
    printTime("Total CPU Workload", globalStart, globalEnd);
}