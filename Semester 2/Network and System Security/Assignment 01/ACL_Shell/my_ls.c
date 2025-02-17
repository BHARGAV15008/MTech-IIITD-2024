#include <stdio.h>
#include <dirent.h>
#include <sys/stat.h>
#include <pwd.h>
#include <unistd.h> // Add this line for getuid, access, and R_OK
#include "aclManager.h"

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: my_ls <directory>\n");
        return 1;
    }

    const char *path = argv[1];

    // Get the current username
    struct passwd *pw = getpwuid(getuid());
    if (!pw) {
        perror("getpwuid");
        return 1;
    }

    // Check ACL and DAC permissions
    if (!checkAcl(path, pw->pw_name, 'r') && access(path, R_OK) != 0) {
        fprintf(stderr, "Access denied\n");
        return 1;
    }

    // Open directory
    DIR *dir = opendir(path);
    if (!dir) {
        perror("opendir");
        return 1;
    }

    // List directory contents
    struct dirent *entry;
    while ((entry = readdir(dir)) != NULL) {
        printf("%s\n", entry->d_name);
    }

    closedir(dir);
    return 0;
}
