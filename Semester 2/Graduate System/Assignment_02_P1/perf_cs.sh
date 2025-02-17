#!/bin/bash

# Output CSV file
output_file="cache_misses_vs_threads.csv"
echo "Threads,Cache_Misses,Cache_References" > $output_file

# Define the workload type (adjust based on your program's expected inputs)
workload="c"  # Change this to "m", "i", or "x" if needed

# Loop over different thread counts
for threads in 2 4 8 16 32; do
    echo "Running with $threads threads..."
    
    # Run perf and extract cache misses and references
    perf stat -e cache-misses -e cache-references -a -o perf_output.txt -- ./pa02 $workload $threads
    
    # Extract values from perf output
    cache_misses=$(grep "cache-misses" perf_output.txt | awk '{print $1}' | tr -d ',')
    cache_references=$(grep "cache-references" perf_output.txt | awk '{print $1}' | tr -d ',')

    # Append to CSV
    echo "$threads,$cache_misses,$cache_references" >> $output_file
done

echo "Cache miss data saved to $output_file"
