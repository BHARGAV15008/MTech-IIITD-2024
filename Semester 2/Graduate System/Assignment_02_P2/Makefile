# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra -pthread -O2
INCLUDES = -Iinclude
LDFLAGS = -pthread

# Directories
SRC_DIR = src
INC_DIR = include
OBJ_DIR = obj
BIN_DIR = bin
REPORT_DIR = report_outputs

# Files
SOURCES = $(wildcard $(SRC_DIR)/*.c)
OBJECTS = $(patsubst $(SRC_DIR)/%.c,$(OBJ_DIR)/%.o,$(SOURCES))
TARGET = $(BIN_DIR)/producer_consumer

# Phony targets
.PHONY: all clean dirs run perf perf-record perf-thread-comparison

# Default target
all: dirs $(TARGET)

# Create directories
dirs:
	@mkdir -p $(OBJ_DIR) $(BIN_DIR) $(REPORT_DIR)

# Link the executable
$(TARGET): $(OBJECTS)
	$(CC) $(OBJECTS) -o $@ $(LDFLAGS)

# Compile source files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

# Explicit compilation for utils.c to avoid redefinition errors
$(OBJ_DIR)/utils.o: $(SRC_DIR)/utils.c
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

# Run the program with default settings
run: $(TARGET)
	./$(TARGET)

# Run with perf for performance analysis
perf: $(TARGET)
	perf stat -e context-switches,cache-misses,cache-references,page-faults,cpu-migrations ./$(TARGET) 4 10 100 > $(REPORT_DIR)/perf_4_threads.txt

# More detailed perf analysis
perf-record: $(TARGET)
	perf record -g ./$(TARGET) 4 10 100
	perf report

# Run tests with varying thread counts for analysis
perf-thread-comparison: $(TARGET)
	@echo "Running thread comparison tests..."
	perf stat -e context-switches,cache-misses,cache-references ./$(TARGET) 1 10 100 > $(REPORT_DIR)/perf_1_threads.txt
	perf stat -e context-switches,cache-misses,cache-references ./$(TARGET) 2 10 100 > $(REPORT_DIR)/perf_2_threads.txt
	perf stat -e context-switches,cache-misses,cache-references ./$(TARGET) 4 10 100 > $(REPORT_DIR)/perf_4_threads.txt
	perf stat -e context-switches,cache-misses,cache-references ./$(TARGET) 8 10 100 > $(REPORT_DIR)/perf_8_threads.txt
	@echo "Thread comparison tests completed. See $(REPORT_DIR) for results."

# Clean up
clean:
	rm -rf $(OBJ_DIR) $(BIN_DIR) $(REPORT_DIR) perf.data perf.data.old
