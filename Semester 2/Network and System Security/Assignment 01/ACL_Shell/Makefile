# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra -std=c99
LDFLAGS =

# Source files
SRCS = main.c aclManager.c fileOperations.c fput.c getacl.c my_cd.c my_ls.c setacl.c
OBJS = $(SRCS:.c=.o)
EXECUTABLES = aclShell fput getacl my_cd my_ls setacl

# Default target
all: $(EXECUTABLES)

# Build each executable
aclShell: main.o aclManager.o fileOperations.o
	$(CC) $(CFLAGS) -o $@ main.o aclManager.o fileOperations.o $(LDFLAGS)

fput: fput.o aclManager.o
	$(CC) $(CFLAGS) -o $@ fput.o aclManager.o $(LDFLAGS)

getacl: getacl.o
	$(CC) $(CFLAGS) -o $@ getacl.o $(LDFLAGS)

my_cd: my_cd.o aclManager.o
	$(CC) $(CFLAGS) -o $@ my_cd.o aclManager.o $(LDFLAGS)

my_ls: my_ls.o aclManager.o
	$(CC) $(CFLAGS) -o $@ my_ls.o aclManager.o $(LDFLAGS)

setacl: setacl.o
	$(CC) $(CFLAGS) -o $@ setacl.o $(LDFLAGS)

# Compile .c files into .o files
%.o: %.c aclManager.h fileOperations.h
	$(CC) $(CFLAGS) -c $< -o $@

# Clean up build files
clean:
	rm -f $(OBJS) $(EXECUTABLES)

.PHONY: all clean
