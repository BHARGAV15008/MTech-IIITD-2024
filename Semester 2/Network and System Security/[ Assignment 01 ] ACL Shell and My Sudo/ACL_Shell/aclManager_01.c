#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#ifdef __FreeBSD__
#include <sys/extattr.h>
#else
#include <sys/xattr.h>
#endif

int checkAcl(const char *path, const char *user, char mode) {
    char aclValue[257]; // Buffer to hold ACL string (+1 for null terminator)
    ssize_t len;

#ifdef __FreeBSD__
    len = extattr_get_file(path, EXTATTR_NAMESPACE_USER, "user.acl", aclValue, sizeof(aclValue) - 1);
#else
    len = getxattr(path, "user.acl", aclValue, sizeof(aclValue) - 1);
#endif

    if (len < 0) {
        return 0; // No ACL, deny access
    }

    if (len >= (ssize_t)(sizeof(aclValue) - 1)) {
        return 0; // ACL value truncated, treat as no ACL
    }

    aclValue[len] = '\0'; // Null-terminate the ACL string

    // Tokenize the ACL string by spaces
    char *token = strtok(aclValue, " ");
    while (token != NULL) {
        // Split the token into username and permissions
        char *comma = strchr(token, ',');
        if (!comma) {
            token = strtok(NULL, " ");
            continue;
        }

        *comma = '\0'; // Split the token into username and permissions
        if (strcmp(token, user) == 0) {
            if (strchr(comma + 1, mode) != NULL) {
                return 1; // ACL allows access
            }
        }

        token = strtok(NULL, " ");
    }

    return 0; // ACL denies access
}
