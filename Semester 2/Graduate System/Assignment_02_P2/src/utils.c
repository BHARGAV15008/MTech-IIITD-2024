#include "utils.h"
#include <stdlib.h>
#include <time.h>

// Start the timer
void timerStart(Timer* timer) {
    clock_gettime(CLOCK_MONOTONIC, &timer->startTime);
}

// Stop the timer
void timerStop(Timer* timer) {
    clock_gettime(CLOCK_MONOTONIC, &timer->endTime);
}

// Calculate elapsed time in seconds
double timerElapsedSeconds(Timer* timer) {
    return (timer->endTime.tv_sec - timer->startTime.tv_sec) + 
           (timer->endTime.tv_nsec - timer->startTime.tv_nsec) / 1.0e9;
}

// Initialize random number generator
void randomInit(void) {
    srand(time(NULL));
}

// Generate a random number within a specified range
int randomRange(int min, int max) {
    return min + rand() % (max - min + 1);
}