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

    // Check ACL and DAC permissions
    if (!checkAcl(path, user, 'r') && access(path, R_OK) != 0) {
        fprintf(stderr, "Access denied: No read permission\n");
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
    if (setresuid(-1, file_owner, file_owner) < 0) {
        perror("setresuid");
        close(fd);
        return;
    }

    // Read file contents
    char buf[4096];
    ssize_t bytes;
    while ((bytes = read(fd, buf, sizeof(buf))) > 0) {
        write(STDOUT_FILENO, buf, bytes);
    }

    // Restore privileges
    if (setresuid(-1, realUid, realUid) < 0) {
        perror("setresuid restore");
    }

    close(fd);
}
