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

    // Check ACL and DAC permissions
    if (!checkAcl(path, pw->pw_name, 'w') && access(path, W_OK) != 0) {
        fprintf(stderr, "Access denied\n");
        return 1;
    }

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
    return 0;
}
