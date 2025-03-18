#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#ifdef __FreeBSD__
#include <sys/extattr.h>
#define ENOATTR ENOENT
#else
#include <sys/xattr.h>
#endif

// Define ENODATA if it is not already defined
#ifndef ENODATA
#define ENODATA 61 // Common value for ENODATA on many systems
#endif

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: getacl <file>\n");
        return 1;
    }

    const char *path = argv[1];

    // Get ACL
    char aclValue[256];
    ssize_t len;

#ifdef __FreeBSD__
    // On FreeBSD, we need to use the USER namespace and the attribute name is just "acl"
    len = extattr_get_file(path, EXTATTR_NAMESPACE_USER, "acl", aclValue, sizeof(aclValue) - 1);
#else
    len = getxattr(path, "user.acl", aclValue, sizeof(aclValue) - 1);
#endif

    if (len < 0) {
        if (errno == ENODATA || errno == ENOATTR) {
            printf("No ACL set for %s\n", path);
        } else {
            perror("getxattr/extattr_get_file");
        }
        return 1;
    }

    aclValue[len] = '\0';
    printf("ACL: %s\n", aclValue);

    return 0;
}
