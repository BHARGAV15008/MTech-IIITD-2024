#include <stdio.h>
#include <unistd.h>
#include <sys/stat.h>
#include <pwd.h>
#include "aclManager.h"

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: my_cd <directory>\n");
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
    if (!checkAcl(path, pw->pw_name, 'x') && access(path, X_OK) != 0) {
        fprintf(stderr, "Access denied\n");
        return 1;
    }

    // Change directory
    if (chdir(path) < 0) {
        perror("chdir");
        return 1;
    }

    return 0;
}
