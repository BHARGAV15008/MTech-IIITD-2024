CC = gcc
CFLAGS = -O3 -mavx2 -mfma -pthread -Wall -Wextra -fopenmp
LDFLAGS = -lnuma -laio
INCLUDES = -Iinclude
SRC_DIR = src
BUILD_DIR = build
TARGET = pa02

SRCS = $(wildcard $(SRC_DIR)/*.c) main.c
OBJS = $(patsubst %.c,$(BUILD_DIR)/%.o,$(SRCS))

all: $(BUILD_DIR) $(TARGET)

$(BUILD_DIR):
	mkdir -p $@

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(INCLUDES) $^ -o $@ $(LDFLAGS)

$(BUILD_DIR)/%.o: %.c | $(BUILD_DIR)
	mkdir -p $(dir $@)
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

clean:
	rm -rf $(BUILD_DIR) $(TARGET)

.PHONY: all clean