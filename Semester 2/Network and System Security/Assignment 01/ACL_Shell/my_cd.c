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
    
    // Debug: Print current user
    printf("Current user: %s\n", pw->pw_name);
    
    // Check ACL permissions first
    int acl_allowed = checkAcl(path, pw->pw_name, 'x');
    printf("ACL check result: %s\n", acl_allowed ? "Allowed" : "Denied");
    
    // Check standard permissions
    int std_allowed = (access(path, X_OK) == 0);
    printf("Standard permission check result: %s\n", std_allowed ? "Allowed" : "Denied");

    // Check ACL and DAC permissions - allow if either permits
    if (acl_allowed || std_allowed) {
        // Change directory
        if (chdir(path) < 0) {
            perror("chdir");
            return 1;
        }
        printf("Changed directory to %s\n", path);
        return 0;
    } else {
        fprintf(stderr, "Access denied: No execute permission on directory '%s'\n", path);
        return 1;
    }
}
