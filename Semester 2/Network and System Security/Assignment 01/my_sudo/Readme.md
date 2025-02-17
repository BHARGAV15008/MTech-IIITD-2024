# my_sudo

## Overview

**my_sudo** is a simplified version of the `sudo` command. It allows users to execute commands with elevated privileges (as root) or switch to the owner of the target program. The program utilizes the `setuid()` and `seteuid()` system calls to manage privileges.

## Requirements

- A Unix-like operating system (Linux, FreeBSD, etc.).
- GCC compiler.
- Root access to set the setuid bit on the `my_sudo` executable.

## Compilation

Compile the `my_sudo` program:

```bash
gcc -o my_sudo my_sudo.c
```

Set the setuid bit and change ownership to root:

```bash
sudo chown root:root my_sudo
sudo chmod 4755 my_sudo
```

## Usage

### Syntax

```bash
./my_sudo <command> [arguments]
```

### Examples

#### Run a command as root:
```bash
./my_sudo ls /root
```

#### Run a command as the owner of the target program:
```bash
./my_sudo ./my_program
```

## Functionality

### Privilege Escalation:
- If the target program is owned by root, `my_sudo` runs it with root privileges.
- If the target program is owned by another user, `my_sudo` switches to that user's privileges using `seteuid()`.

### Corner Cases Handled:
- **Invalid Command**: If the command does not exist, an error message is displayed.
- **Permission Denied**: If the user does not have execute permission for the target program, access is denied.
- **Setuid Failure**: If `setuid()` or `seteuid()` fails, the program exits with an error.

## Assumptions

- The `my_sudo` program is owned by root and has the setuid bit set.
- The target program exists and is executable.
- The user running `my_sudo` has permission to execute the target program.

## Code Example

Here is the `my_sudo.c` program:

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <errno.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <command> [arguments]\n", argv[0]);
        exit(1);
    }

    // Get the target program path
    char *program = argv[1];
    struct stat st;

    // Check if the target program exists
    if (stat(program, &st) < 0) {
        perror("stat");
        exit(1);
    }

    // Get the owner of the target program
    uid_t owner = st.st_uid;

    // If the target program is owned by root, run as root
    if (owner == 0) {
        if (setuid(0) < 0) {
            perror("setuid");
            exit(1);
        }
    } else {
        // Otherwise, switch to the owner of the target program
        if (seteuid(owner) < 0) {
            perror("seteuid");
            exit(1);
        }
    }

    // Execute the target program
    execvp(program, &argv[1]);

    // If execvp fails
    perror("execvp");
    exit(1);
}
```

## Testing

### Test Case 1: Run a Command as Root

#### Create a file owned by root:
```bash
sudo touch /root/testfile
```

#### Run `my_sudo` to list the contents of `/root`:
```bash
./my_sudo ls /root
```

**Expected Output**: The contents of `/root` are displayed.

### Test Case 2: Run a Command as Another User

#### Create a file owned by another user:
```bash
sudo -u nobody touch /tmp/nobodyfile
```

#### Run `my_sudo` to list the file:
```bash
./my_sudo ls /tmp/nobodyfile
```

**Expected Output**: The file `/tmp/nobodyfile` is listed.

### Test Case 3: Invalid Command

#### Run `my_sudo` with a non-existent command:
```bash
./my_sudo invalid_command
```

**Expected Output**: An error message is displayed (e.g., `execvp: No such file or directory`).

### Test Case 4: Permission Denied

#### Create a file without execute permission:
```bash
touch no_permission_file
chmod -x no_permission_file
```

#### Run `my_sudo` to execute the file:
```bash
./my_sudo ./no_permission_file
```

**Expected Output**: An error message is displayed (e.g., `Permission denied`).

## Defended Attacks/Errors

- **Privilege Escalation**: Prevented by ensuring `my_sudo` only escalates privileges for programs owned by root or switches to the owner of the target program.
- **Invalid Commands**: Handled by checking if the target program exists and is executable.
- **Permission Denied**: Handled by checking file permissions before executing the target program.

## Notes

- Ensure `my_sudo` is always owned by root and has the setuid bit set.
- Use caution when running `my_sudo` with untrusted programs, as it can escalate privileges.

