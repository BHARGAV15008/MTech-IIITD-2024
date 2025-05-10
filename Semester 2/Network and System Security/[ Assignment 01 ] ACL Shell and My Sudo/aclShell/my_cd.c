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
    int acl_allowed = checkAcl(path, pw->pw_name, 'x');
    int dac_allowed = (access(path, X_OK) == 0);

    printf("ACL permission: %s\n", acl_allowed ? "Allowed" : "Denied or not set");
    printf("DAC permission: %s\n", dac_allowed ? "Allowed" : "Denied");

    if (!acl_allowed && !dac_allowed) {
        fprintf(stderr, "Access denied: No execute permission on directory\n");
        return 1;
    }

    // Change directory
    if (chdir(path) < 0) {
        perror("chdir");
        return 1;
    }

    printf("Changed to directory: %s\n", path);
    return 0;
}
