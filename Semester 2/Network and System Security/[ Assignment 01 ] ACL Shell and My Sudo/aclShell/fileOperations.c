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
    int acl_allowed = checkAcl(path, user, 'r');
    int dac_allowed = (access(path, R_OK) == 0);

    printf("ACL permission: %s\n", acl_allowed ? "Allowed" : "Denied or not set");
    printf("DAC permission: %s\n", dac_allowed ? "Allowed" : "Denied");

    if (!acl_allowed && !dac_allowed) {
        fprintf(stderr, "Access denied: No read permission\n");
        return;
    }

    // Open the file with O_NOFOLLOW to prevent symlink attacks
    int fd = open(path, O_RDONLY | O_NOFOLLOW);
    if (fd < 0) {
        perror("open");
        return;
    }

    // Get file info
    struct stat st;
    if (fstat(fd, &st) < 0) {
        perror("fstat");
        close(fd);
        return;
    }

    // Read file contents
    char buf[4096];
    ssize_t bytes;
    printf("\n--- File Contents of %s ---\n", path);
    while ((bytes = read(fd, buf, sizeof(buf))) > 0) {
        write(STDOUT_FILENO, buf, bytes);
    }

    if (bytes < 0) {
        perror("read");
    }

    printf("\n--- End of File Contents ---\n");
    close(fd);
}
