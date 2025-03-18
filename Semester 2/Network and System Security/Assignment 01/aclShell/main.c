#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <pwd.h>
#include "aclManager.h"
#include "fileOperations.h"

void printHelp() {
    printf("\nACL Shell Help:\n");
    printf("----------------\n");
    printf("fget <file>                   - Read contents of a file\n");
    printf("fput <file>                   - Append data to a file\n");
    printf("my_ls <directory>             - List directory contents\n");
    printf("my_cd <directory>             - Change current directory\n");
    printf("create_dir <directory>        - Create a new directory\n");
    printf("setacl <file> <user,perm>     - Set ACL permissions (e.g., user1,rw)\n");
    printf("getacl <file>                 - Get ACL permissions\n");
    printf("pwd                           - Show current directory\n");
    printf("help                          - Show this help\n");
    printf("exit                          - Exit the ACL Shell\n");
    printf("\nPermission characters: r (read), w (write), x (execute)\n");
}

void aclShell() {
    struct passwd *pw = getpwuid(getuid());
    char current_dir[1024];
    char command[256];

    printf("\nWelcome to ACL Shell! Type 'help' for available commands.\n");

    while (1) {
        // Get current directory for prompt
        if (getcwd(current_dir, sizeof(current_dir)) == NULL) {
            strcpy(current_dir, "unknown");
        }

        printf("\n%s@ACLShell:%s> ", pw ? pw->pw_name : "user", current_dir);
        if (!fgets(command, sizeof(command), stdin)) break;

        // Remove newline character
        command[strcspn(command, "\n")] = 0;

        // Skip empty commands
        if (strlen(command) == 0) continue;

        // Parse command and arguments
        char *cmd = strtok(command, " ");
        char *arg = strtok(NULL, "");

        if (cmd && strcmp(cmd, "fget") == 0 && arg) {
            fget(arg); // fget is implemented in fileOperations.c
        } else if (cmd && strcmp(cmd, "help") == 0) {
            printHelp();
        } else if (cmd && strcmp(cmd, "pwd") == 0) {
            printf("Current directory: %s\n", current_dir);
        } else if (cmd && strcmp(cmd, "exit") == 0) {
            printf("Exiting ACL Shell. Goodbye!\n");
            break;
        } else if (cmd) {
            // Handle external commands (my_ls, fput, my_cd, etc.)
            pid_t pid = fork();
            if (pid == 0) {
                // Child process: execute the command
                if (strcmp(cmd, "my_ls") == 0) {
                    execlp("./my_ls", "my_ls", arg ? arg : ".", NULL);
                } else if (strcmp(cmd, "fput") == 0) {
                    execlp("./fput", "fput", arg, NULL);
                } else if (strcmp(cmd, "my_cd") == 0) {
                    execlp("./my_cd", "my_cd", arg, NULL);
                } else if (strcmp(cmd, "create_dir") == 0) {
                    execlp("./create_dir", "create_dir", arg, NULL);
                } else if (strcmp(cmd, "setacl") == 0) {
                    // Parse two arguments for setacl
                    char *file = arg;
                    char *acl_entry = NULL;

                    if (file) {
                        // Find the first space after file
                        acl_entry = strchr(file, ' ');
                        if (acl_entry) {
                            *acl_entry = '\0'; // Split the string
                            acl_entry++; // Move past the space
                        }
                    }

                    if (file && acl_entry) {
                        execlp("./setacl", "setacl", file, acl_entry, NULL);
                    } else {
                        fprintf(stderr, "Usage: setacl <file> <user,permissions>\n");
                        exit(1);
                    }
                } else if (strcmp(cmd, "getacl") == 0) {
                    execlp("./getacl", "getacl", arg, NULL);
                } else {
                    fprintf(stderr, "Unknown command: %s\n", cmd);
                    fprintf(stderr, "Type 'help' for a list of available commands.\n");
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
