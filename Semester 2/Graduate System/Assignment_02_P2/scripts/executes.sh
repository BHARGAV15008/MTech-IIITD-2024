#!/bin/bash

# Configuration
PROGRAM="./bin/producer_consumer"
REPORT_DIR="report_outputs"
PLOT_DIR="plots"
THREAD_COUNTS=(1 2 4 8 16)
BUFFER_SIZES=(10 50 100)
ITEMS_PER_PRODUCER=1000

# Create directories
mkdir -p "$REPORT_DIR" "$PLOT_DIR"

run_thread_comparison() {
    echo "Running thread comparison for buffer $1..."
    CSV_FILE="$REPORT_DIR/thread_comparison_buffer_$1.csv"
    
    # CSV Header
    echo "Threads,ExecutionTime,Throughput,ContextSwitches,CacheMisses,CacheReferences" > "$CSV_FILE"
    
    for threads in "${THREAD_COUNTS[@]}"; do
        echo "Testing $threads threads..."
        
        PERF_OUTPUT=$(perf stat -e context-switches,cache-misses,cache-references \
            $PROGRAM $threads $1 $ITEMS_PER_PRODUCER 2>&1)
        
        # Extract metrics
        EXEC_TIME=$(echo "$PERF_OUTPUT" | awk '/Execution time:/ {print $3}')
        THROUGHPUT=$(echo "$PERF_OUTPUT" | awk '/Throughput:/ {print $2}')
        CONTEXT_SWITCHES=$(echo "$PERF_OUTPUT" | awk '/context-switches/ {gsub(/,/,""); print $1}')
        CACHE_MISSES=$(echo "$PERF_OUTPUT" | awk '/cache-misses/ {gsub(/,/,""); print $1}')
        CACHE_REFERENCES=$(echo "$PERF_OUTPUT" | awk '/cache-references/ {gsub(/,/,""); print $1}')
        
        # Save to CSV
        echo "$threads,$EXEC_TIME,$THROUGHPUT,$CONTEXT_SWITCHES,$CACHE_MISSES,$CACHE_REFERENCES" >> "$CSV_FILE"
        
        # Save raw perf output
        echo "$PERF_OUTPUT" > "$REPORT_DIR/perf_${threads}_threads_buffer_$1.txt"
    done
}

# Main execution
echo "=== Starting Performance Analysis ==="
make clean && make

# Run tests for all buffer sizes
for buffer in "${BUFFER_SIZES[@]}"; do
    run_thread_comparison $buffer
done

# Generate Python plots
echo "Generating Python visualizations..."
python3 scripts/plot_metrics.py
python3 scripts/interactive_plot.py

echo "=== Analysis Complete ==="
echo "CSV Files: $REPORT_DIR/"
echo "Plots: $PLOT_DIR/"
