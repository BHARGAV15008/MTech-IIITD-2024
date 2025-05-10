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
    
    // Debug: Print current user
    printf("Current user: %s\n", pw->pw_name);

    // Check ACL permissions first
    int acl_allowed = checkAcl(path, pw->pw_name, 'r');
    printf("ACL check result: %s\n", acl_allowed ? "Allowed" : "Denied");
    
    // Check standard permissions
    int std_allowed = (access(path, R_OK) == 0);
    printf("Standard permission check result: %s\n", std_allowed ? "Allowed" : "Denied");

    // Check ACL and DAC permissions - allow if either permits
    if (acl_allowed || std_allowed) {
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
    } else {
        fprintf(stderr, "Access denied: No read permission on directory '%s'\n", path);
        return 1;
    }
}
