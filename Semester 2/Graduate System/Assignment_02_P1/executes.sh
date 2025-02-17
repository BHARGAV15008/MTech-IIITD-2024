#!/bin/bash

runPerfAnalysis() {
    program=$1
    threads=$2
    echo "Running perf analysis for $program with $threads threads..."
    perf stat -e cpu-migrations,branch-misses,L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores,LLC-loads,LLC-load-misses,LLC-stores,LLC-prefetches ./pa02 $program $threads
	perf stat -d ./pa02 $program $threads
	perf stat -e cpu-clock,iowait ./pa02 $program $threads
	perf stat -e task-clock,cycles,instructions,cache-references,cache-misses,branches,branch-misses,context-switches,cpu-migrations ./pa02 $program $threads

}

# Part A: Scalability tests
for threads in 2 4 6 8 12 16 18 32; do
    runPerfAnalysis c $threads
    runPerfAnalysis m $threads
    runPerfAnalysis i $threads
    runPerfAnalysis x $threads
done
