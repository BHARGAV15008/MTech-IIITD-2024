#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>
#include <pwd.h>
#include "aclManager.h"

void fget(const char *path) {
    uid_t realUid = getuid();

    // Get the current username
    struct passwd *pw = getpwuid(realUid);
    if (!pw) {
        perror("getpwuid");
        return;
    }

    const char *user = pw->pw_name;
    
    // Debug: Print current user
    printf("Current user: %s\n", user);

    // Check ACL permissions first
    int acl_allowed = checkAcl(path, user, 'r');
    printf("ACL check result: %s\n", acl_allowed ? "Allowed" : "Denied");
    
    // Check standard permissions
    int std_allowed = (access(path, R_OK) == 0);
    printf("Standard permission check result: %s\n", std_allowed ? "Allowed" : "Denied");

    // Check ACL and DAC permissions - allow if either permits
    if (!(acl_allowed || std_allowed)) {
        fprintf(stderr, "Access denied: No read permission on file '%s'\n", path);
        return;
    }

    // Open the file with O_NOFOLLOW to prevent symlink attacks
    int fd = open(path, O_RDONLY | O_NOFOLLOW);
    if (fd < 0) {
        perror("open");
        return;
    }

    // Get file owner and drop privileges
    struct stat st;
    if (fstat(fd, &st) < 0) {
        perror("fstat");
        close(fd);
        return;
    }

    uid_t file_owner = st.st_uid;
    // Only drop privileges if we're running as root
    if (realUid == 0) {
        if (setresuid(-1, file_owner, realUid) < 0) {
            perror("setresuid");
            close(fd);
            return;
        }
    }

    // Read file contents
    char buf[4096];
    ssize_t bytes;
    while ((bytes = read(fd, buf, sizeof(buf))) > 0) {
        write(STDOUT_FILENO, buf, bytes);
    }

    // Restore privileges if we dropped them
    if (realUid == 0) {
        if (setresuid(-1, realUid, realUid) < 0) {
            perror("setresuid restore");
        }
    }

    close(fd);
}
