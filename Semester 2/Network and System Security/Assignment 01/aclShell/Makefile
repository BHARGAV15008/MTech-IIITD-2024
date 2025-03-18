# Compiler and flags for FreeBSD
CC = cc
CFLAGS = -Wall -Wextra -O2 -g -std=c99
LDFLAGS =

# Source files
SRCS = main.c aclManager.c fileOperations.c my_ls.c my_cd.c fput.c getacl.c setacl.c create_dir.c
OBJS = $(SRCS:.c=.o)
EXECS = aclShell my_ls my_cd fput getacl setacl create_dir

# Default target
all: $(EXECS)

# Build the ACL shell
aclShell: main.o aclManager.o fileOperations.o
	$(CC) $(CFLAGS) -o $@ main.o aclManager.o fileOperations.o $(LDFLAGS)

# Build my_ls
my_ls: my_ls.o aclManager.o
	$(CC) $(CFLAGS) -o $@ my_ls.o aclManager.o $(LDFLAGS)

# Build my_cd
my_cd: my_cd.o aclManager.o
	$(CC) $(CFLAGS) -o $@ my_cd.o aclManager.o $(LDFLAGS)

# Build fput
fput: fput.o aclManager.o
	$(CC) $(CFLAGS) -o $@ fput.o aclManager.o $(LDFLAGS)

# Build getacl
getacl: getacl.o
	$(CC) $(CFLAGS) -o $@ getacl.o $(LDFLAGS)

# Build setacl
setacl: setacl.o
	$(CC) $(CFLAGS) -o $@ setacl.o $(LDFLAGS)

# Build create_dir
create_dir: create_dir.o aclManager.o
	$(CC) $(CFLAGS) -o $@ create_dir.o aclManager.o $(LDFLAGS)

# Compile .c files into .o files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Clean up build files
clean:
	rm -f $(OBJS) $(EXECS)

# Phony targets
.PHONY: all clean
