#define _GNU_SOURCE  // Must be first line
#include "../include/IoWorkload.h"
#include "../include/Common.h"
#include <fcntl.h>
#include <libaio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int fileDesc;
    void* buffer;
    size_t size;
} IoThreadData;

static void* ioWorker(void* arg) {
    IoThreadData* d = (IoThreadData*)arg;
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    io_context_t ctx = 0;
    struct iocb cb;
    struct iocb* cbs[1] = {&cb};

    if(io_setup(1, &ctx) < 0) {
        perror("io_setup failed");
        return NULL;
    }

    for(size_t offset = 0; offset < d->size; offset += 4096) {
        io_prep_pwrite(&cb, d->fileDesc, d->buffer + offset, 4096, offset);
        
        if(io_submit(ctx, 1, cbs) != 1) {
            perror("io_submit failed");
            break;
        }

        struct io_event ev;
        if(io_getevents(ctx, 1, 1, &ev, NULL) != 1) {
            perror("io_getevents failed");
            break;
        }
    }

    io_destroy(ctx);
    clock_gettime(CLOCK_MONOTONIC, &end);
    printTime("I/O Thread", start, end);
    return NULL;
}

void runIoWorkload(int threadCount) {
    pthread_t workers[threadCount];
    IoThreadData threadData[threadCount];
    const size_t size = 1UL << 30; // 1GB

    struct timespec globalStart, globalEnd;
    clock_gettime(CLOCK_MONOTONIC, &globalStart);

    // Create and truncate file
    int fd = open("/tmp/iofile", O_CREAT | O_TRUNC | O_WRONLY, 0644);
    close(fd);

    for(int i = 0; i < threadCount; i++) {
        threadData[i].fileDesc = open("/tmp/iofile", 
                                    O_DIRECT | O_RDWR | O_SYNC,
                                    0644);
        if(threadData[i].fileDesc < 0) {
            perror("open failed");
            exit(EXIT_FAILURE);
        }

        if(posix_memalign(&threadData[i].buffer, 4096, size/threadCount) != 0) {
            perror("posix_memalign failed");
            exit(EXIT_FAILURE);
        }
        
        memset(threadData[i].buffer, rand(), size/threadCount);
        threadData[i].size = size/threadCount;
        
        if(pthread_create(&workers[i], NULL, ioWorker, &threadData[i]) != 0) {
            perror("pthread_create failed");
            exit(EXIT_FAILURE);
        }
    }

    for(int i = 0; i < threadCount; i++) {
        pthread_join(workers[i], NULL);
        close(threadData[i].fileDesc);
        free(threadData[i].buffer);
    }

    clock_gettime(CLOCK_MONOTONIC, &globalEnd);
    printTime("Total I/O Workload", globalStart, globalEnd);
}