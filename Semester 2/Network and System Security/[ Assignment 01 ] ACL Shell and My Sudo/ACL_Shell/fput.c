#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <pwd.h>
#include <string.h> // Add this line
#include "aclManager.h"

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: fput <file>\n");
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
    int acl_allowed = checkAcl(path, pw->pw_name, 'w');
    printf("ACL check result: %s\n", acl_allowed ? "Allowed" : "Denied");
    
    // Check standard permissions
    int std_allowed = (access(path, W_OK) == 0);
    printf("Standard permission check result: %s\n", std_allowed ? "Allowed" : "Denied");

    // Check ACL and DAC permissions - allow if either permits
    if (acl_allowed || std_allowed) {
        // Open file for appending
        int fd = open(path, O_WRONLY | O_APPEND | O_NOFOLLOW);
        if (fd < 0) {
            perror("open");
            return 1;
        }

        // Write to file
        const char *data = "Appended data\n";
        write(fd, data, strlen(data));

        close(fd);
        printf("Data appended to file '%s'\n", path);
        return 0;
    } else {
        fprintf(stderr, "Access denied: No write permission on file '%s'\n", path);
        return 1;
    }
}
