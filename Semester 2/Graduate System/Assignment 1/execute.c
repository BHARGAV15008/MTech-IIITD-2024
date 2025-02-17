#include "execute.h"

int execute_command(char *cmd, char **args) {
    if (cmd == NULL) {
        fprintf(stderr, "Command not found\n");
        return -1;
    }

    if (strcmp(cmd, "cd") == 0) {
        if (args[1] == NULL) {
            char *home_dir = getenv("HOME");
            if (home_dir) {
                chdir(home_dir);
            } else {
                perror("cd failed");
            }
        } else {
            if (chdir(args[1]) != 0) {
                perror("cd failed");
            }
        }
        return 0;
    }

    if (strcmp(cmd, "ls") == 0) {
        ls_command(args);
        return 0;
    }

    if (strcmp(cmd, "help") == 0) {
        help_command(args);
        return 0;
    }

    pid_t pid = fork();
    if (pid < 0) {
        perror("fork failed");
        return -1;
    }

    if (pid == 0) {
        if (execvp(cmd, args) == -1) {
            perror("execvp failed");
        }
        exit(1);
    } else {
        int status;
        waitpid(pid, &status, 0);
        return status;
    }
}

void ls_command(char **args) {
    char *command = "ls";
    execvp(command, args);
}

void help_command(char **args) {
    printf("Available commands: ls, cd, exit, help\n");
}