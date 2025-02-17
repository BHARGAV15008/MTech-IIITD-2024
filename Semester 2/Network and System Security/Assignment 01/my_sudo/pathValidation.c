#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <limits.h>
#include <errno.h>
#include <syslog.h>
#include "pathValidation.h"

char* resolveSecurePath(const char *inputPath) {
    char *resolved = realpath(inputPath, NULL);
    if (!resolved) {
        syslog(LOG_ERR, "Path resolution failed: %s", strerror(errno));
        return NULL;
    }

    // Check against allowed paths
    const char *allowedPaths[] = {"/usr/bin/", "/bin/", "/sbin/"};
    int valid = 0;
    for (int i = 0; i < 3; i++) {
        if (strncmp(resolved, allowedPaths[i], strlen(allowedPaths[i])) == 0) {
            valid = 1;
            break;
        }
    }

    if (!valid) {
        syslog(LOG_ALERT, "Path violation: %s", resolved);
        free(resolved);
        return NULL;
    }

    // Check file ownership and permissions
    struct stat st;
    if (lstat(resolved, &st) < 0) {
        syslog(LOG_ERR, "lstat failed: %s", strerror(errno));
        free(resolved);
        return NULL;
    }

    if ((st.st_mode & S_ISUID) && (st.st_uid != 0)) {
        syslog(LOG_ALERT, "Dangerous SETUID binary: %s", resolved);
        free(resolved);
        return NULL;
    }

    return resolved;
}

uid_t getFileOwnerUid(const char *path) {
    struct stat st;
    if (stat(path, &st) < 0) {
        syslog(LOG_ERR, "stat failed: %s", strerror(errno));
        exit(EXIT_FAILURE);
    }
    return st.st_uid;
}
