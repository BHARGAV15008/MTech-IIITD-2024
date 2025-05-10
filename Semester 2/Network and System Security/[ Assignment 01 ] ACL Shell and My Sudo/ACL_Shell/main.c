#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include "aclManager.h"
#include "fileOperations.h"

void aclShell() {
    char command[256];
    while (1) {
        printf("ACLShell> ");
        if (!fgets(command, sizeof(command), stdin)) break;

        // Remove newline character
        command[strcspn(command, "\n")] = 0;

        // Parse command and arguments
        char *cmd = strtok(command, " ");
        char *arg1 = strtok(NULL, " ");
        char *arg2 = strtok(NULL, " ");
        char *arg3 = strtok(NULL, " ");

        if (cmd && strcmp(cmd, "fget") == 0 && arg1) {
            fget(arg1);
        } else if (cmd && strcmp(cmd, "exit") == 0) {
            break;
        } else if (cmd) {
            // Handle external commands (my_ls, fput, my_cd, etc.)
            pid_t pid = fork();
            if (pid == 0) {
                // Child process: execute the command
                if (strcmp(cmd, "my_ls") == 0) {
                    execlp("./my_ls", "my_ls", arg1, NULL);
                } else if (strcmp(cmd, "fput") == 0) {
                    execlp("./fput", "fput", arg1, NULL);
                } else if (strcmp(cmd, "my_cd") == 0) {
                    execlp("./my_cd", "my_cd", arg1, NULL);
                } else if (strcmp(cmd, "create_dir") == 0) {
                    execlp("./create_dir", "create_dir", arg1, NULL);
                } else if (strcmp(cmd, "setacl") == 0) {
                    execlp("./setacl", "setacl", arg1, arg2, arg3, NULL);
                } else if (strcmp(cmd, "getacl") == 0) {
                    execlp("./getacl", "getacl", arg1, NULL);
                } else {
                    fprintf(stderr, "Unknown command: %s\n", cmd);
                    exit(1);
                }
                // If exec fails
                perror("exec");
                exit(1);
            } else if (pid > 0) {
                // Parent process: wait for the child to finish
                int status;
                waitpid(pid, &status, 0);
            } else {
                perror("fork");
            }
        } else {
            fprintf(stderr, "Unknown command\n");
        }
    }
}

int main() {
    aclShell();
    return 0;
}
