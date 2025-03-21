#include <stdio.h>
#include <sys/stat.h>
#include <pwd.h>
#include <unistd.h>
#include "aclManager.h"

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: create_dir <directory>\n");
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
    if (!checkAcl(path, pw->pw_name, 'w') && access(path, W_OK) != 0) {
        fprintf(stderr, "Access denied\n");
        return 1;
    }

    // Create directory
    if (mkdir(path, 0755) < 0) {
        perror("mkdir");
        return 1;
    }

    return 0;
}
