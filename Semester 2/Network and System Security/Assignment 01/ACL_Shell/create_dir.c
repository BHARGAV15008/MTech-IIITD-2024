#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <pwd.h>
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
    
    // Debug: Print current user
    printf("Current user: %s\n", pw->pw_name);

    // Determine the parent directory
    char parentPath[1024];
    strncpy(parentPath, path, sizeof(parentPath) - 1);
    parentPath[sizeof(parentPath) - 1] = '\0';

    char *lastSlash = strrchr(parentPath, '/');
    if (lastSlash) {
        *lastSlash = '\0'; // Truncate at the last slash to get the parent directory
    } else {
        // If no slash, the parent directory is the current directory
        strcpy(parentPath, ".");
    }
    
    // Debug: Print parent directory path
    printf("Parent directory: %s\n", parentPath);

    // Check ACL permissions first
    int acl_allowed = checkAcl(parentPath, pw->pw_name, 'w'); // Corrected mode to 'w'
    printf("ACL check result: %s\n", acl_allowed ? "Allowed" : "Denied");
    
    // Check standard permissions
    int std_allowed = (access(parentPath, W_OK) == 0);
    printf("Standard permission check result: %s\n", std_allowed ? "Allowed" : "Denied");

    // Check ACL and DAC permissions on the parent directory
    // Change to OR logic - allow if either ACL or standard permissions allow
    if (acl_allowed || std_allowed) {
        // Create directory
        if (mkdir(path, 0755) < 0) {
            perror("mkdir");
            return 1;
        }
        printf("Directory '%s' created successfully.\n", path);
        return 0;
    } else {
        fprintf(stderr, "Access denied: No write permission on parent directory '%s'\n", parentPath);
        return 1;
    }
}

