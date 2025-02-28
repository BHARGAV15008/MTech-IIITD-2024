#ifndef UTILS_H
#define UTILS_H

#include <time.h>

// Timing utilities
typedef struct {
    struct timespec startTime;
    struct timespec endTime;
} Timer;

void timerStart(Timer* timer);
void timerStop(Timer* timer);
double timerElapsedSeconds(Timer* timer);

// Random number utilities
void randomInit(void);
int randomRange(int min, int max);

#endif // UTILS_H