#include "redir.h"

int has_redirection(char **args) {
    for (int i = 0; args[i] != NULL; i++) {
        if (strcmp(args[i], "<") == 0 || strcmp(args[i], ">") == 0) {
            return 1;
        }
    }
    return 0;
}

void handle_redirection(char **args) {
    int i = 0;
    int fd;
    char *file;
    char **cmd_args = malloc(100 * sizeof(char *));
    
    while (args[i] != NULL && strcmp(args[i], "<") != 0 && strcmp(args[i], ">") != 0) {
        cmd_args[i] = args[i];
        i++;
    }
    cmd_args[i] = NULL;

    if (strcmp(args[i], ">") == 0) {
        file = args[i + 1];
        fd = open(file, O_WRONLY | O_CREAT | O_TRUNC, 0644);
        if (fd == -1) {
            perror("open failed");
            return;
        }
        dup2(fd, STDOUT_FILENO);
        close(fd);
    } else if (strcmp(args[i], "<") == 0) {
        file = args[i + 1];
        fd = open(file, O_RDONLY);
        if (fd == -1) {
            perror("open failed");
            return;
        }
        dup2(fd, STDIN_FILENO);
        close(fd);
    }

    execute_command(cmd_args[0], cmd_args);
    free(cmd_args);
}