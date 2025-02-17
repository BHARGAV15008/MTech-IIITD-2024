#include "../include/Common.h"

void printTime(const char* label, struct timespec start, struct timespec end) {
    double duration = (end.tv_sec - start.tv_sec) + 
                     (end.tv_nsec - start.tv_nsec) / 1e9;
    printf("[TIMING] %s: %.4f seconds\n", label, duration);
}

int parseThreadCount(int argc, char* argv[]) {
    if(argc < 3) {
        fprintf(stderr, "Usage: %s <workload> <threads>\n", argv[0]);
        exit(EXIT_FAILURE);
    }
    int count = atoi(argv[2]);
    return (count > 0) ? count : 1;
}