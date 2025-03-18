#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#ifdef __FreeBSD__
#include <sys/extattr.h>
#else
#include <sys/xattr.h>
#endif

// Define ENODATA if it is not already defined
#ifndef ENODATA
#define ENODATA 61 // Common value for ENODATA on many systems
#endif

// Define ENOATTR if it is not already defined
#ifndef ENOATTR
#define ENOATTR 93 // Common value for ENOATTR on many systems
#endif

int checkAcl(const char *path, const char *user, char mode) {
    char aclValue[257]; // Buffer to hold ACL string (+1 for null terminator)
    ssize_t len;

    printf("Checking ACL for path: %s, user: %s, mode: %c\n", path, user, mode);

#ifdef __FreeBSD__
    // On FreeBSD, we need to use the USER namespace
    len = extattr_get_file(path, EXTATTR_NAMESPACE_USER, "acl", aclValue, sizeof(aclValue) - 1);
#else
    len = getxattr(path, "user.acl", aclValue, sizeof(aclValue) - 1);
#endif

    if (len < 0) {
        int err = errno;
        printf("Error getting extended attribute: %s (errno: %d)\n", strerror(err), err);
        // On FreeBSD, ENOATTR is used instead of ENODATA
        if (err == ENODATA || err == ENOATTR || err == ENOENT) {
            printf("No ACL attribute found\n");
            return 0; // No ACL, deny access
        }
        return 0;
    }

    if (len >= (ssize_t)(sizeof(aclValue) - 1)) {
        printf("ACL value too long (truncated)\n");
        return 0; // ACL value truncated, treat as no ACL
    }

    aclValue[len] = '\0'; // Null-terminate the ACL string
    printf("Found ACL: %s\n", aclValue);

    // Tokenize the ACL string by spaces
    char *saveptr;
    char *acl_copy = strdup(aclValue); // Create a copy for strtok_r
    if (!acl_copy) {
        perror("strdup");
        return 0;
    }
    
    char *token = strtok_r(acl_copy, " ", &saveptr);
    while (token != NULL) {
        printf("Processing ACL token: %s\n", token);
        
        // Split the token into username and permissions
        char *comma = strchr(token, ',');
        if (!comma) {
            printf("Invalid ACL format (no comma)\n");
            token = strtok_r(NULL, " ", &saveptr);
            continue;
        }

        *comma = '\0'; // Split the token into username and permissions
        printf("Username: %s, Permissions: %s\n", token, comma + 1);
        
        if (strcmp(token, user) == 0) {
            printf("Username match found\n");
            if (strchr(comma + 1, mode) != NULL) {
                printf("Permission match found\n");
                free(acl_copy);
                return 1; // ACL allows access
            } else {
                printf("Permission not found in ACL\n");
            }
        }

        token = strtok_r(NULL, " ", &saveptr);
    }

    free(acl_copy);
    printf("No matching ACL entry found\n");
    return 0; // ACL denies access
}
