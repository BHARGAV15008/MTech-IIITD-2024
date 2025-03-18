#include <stdio.h>
#include <sys/stat.h>
#include <pwd.h>
#include <unistd.h>
#include <libgen.h> // For dirname()
#include <string.h> // For strdup()
#include "aclManager.h"

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: create_dir <directory>\n");
        return 1;
    }

    const char *path = argv[1];

    // Get parent directory path to check permissions on
    char *path_copy = strdup(path);
    if (!path_copy) {
        perror("strdup");
        return 1;
    }
    char *parent_dir = dirname(path_copy);

    // Get the current username
    struct passwd *pw = getpwuid(getuid());
    if (!pw) {
        perror("getpwuid");
        free(path_copy);
        return 1;
    }

    printf("Checking ACL permissions for user %s on parent directory: %s\n", pw->pw_name, parent_dir);
    if (!checkAcl(parent_dir, pw->pw_name, 'w') && access(parent_dir, W_OK) != 0) {
        fprintf(stderr, "Access denied: Cannot write to parent directory\n");
        free(path_copy);
        return 1;
    }

    free(path_copy); // Free the duplicated path string

    printf("Creating directory: %s\n", path);
    if (mkdir(path, 0755) < 0) {
        perror("mkdir");
        return 1;
    }

    printf("Directory created successfully: %s\n", path);
    return 0;
}
