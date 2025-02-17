#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>
#include <numa.h>
#include <unistd.h>
#include <fcntl.h>
#include <libaio.h>
#include <string.h>
#include <immintrin.h>

void printTime(const char* label, struct timespec start, struct timespec end);
int parseThreadCount(int argc, char* argv[]);