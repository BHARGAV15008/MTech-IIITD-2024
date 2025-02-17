#include "CpuWorkload.h"
#include "MemWorkload.h"
#include "IoWorkload.h"
#include "MixedWorkload.h"
#include "Common.h"

int main(int argc, char* argv[]) {
    if(argc < 3) {
        fprintf(stderr, "Usage: %s <workload> <threads>\n", argv[0]);
        return 1;
    }

    const int threadCount = parseThreadCount(argc, argv);

    switch(argv[1][0]) {
        case 'c': runCpuWorkload(threadCount); break;
        case 'm': runMemWorkload(threadCount); break;
        case 'i': runIoWorkload(threadCount); break;
        case 'x': runMixedWorkload(threadCount); break;
        default: fprintf(stderr, "Invalid workload type\n");
    }

    return 0;
}
