#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <pwd.h>
#include <string.h>
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

    // Check ACL and DAC permissions
    int acl_allowed = checkAcl(path, pw->pw_name, 'w');
    int dac_allowed = (access(path, W_OK) == 0);

    printf("ACL permission: %s\n", acl_allowed ? "Allowed" : "Denied or not set");
    printf("DAC permission: %s\n", dac_allowed ? "Allowed" : "Denied");

    if (!acl_allowed && !dac_allowed) {
        fprintf(stderr, "Access denied: No write permission\n");
        return 1;
    }

    // Open file for appending
    int fd = open(path, O_WRONLY | O_APPEND | O_NOFOLLOW);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    // Write to file
    printf("Enter data to append (CTRL+D to finish):\n");
    char buffer[4096];
    ssize_t bytes_read;

    while ((bytes_read = read(STDIN_FILENO, buffer, sizeof(buffer))) > 0) {
        if (write(fd, buffer, bytes_read) != bytes_read) {
            perror("write");
            close(fd);
            return 1;
        }
    }

    close(fd);
    printf("Data appended successfully to %s\n", path);
    return 0;
}
