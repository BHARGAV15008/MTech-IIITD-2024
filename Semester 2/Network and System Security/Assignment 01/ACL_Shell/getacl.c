#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifdef __FreeBSD__
#include <sys/extattr.h>
#else
#include <sys/xattr.h>
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
    len = extattr_get_file(path, EXTATTR_NAMESPACE_USER, "user.acl", aclValue, sizeof(aclValue) - 1);
#else
    len = getxattr(path, "user.acl", aclValue, sizeof(aclValue) - 1);
#endif

    if (len < 0) {
        perror("getxattr/extattr_get_file");
        return 1;
    }

    aclValue[len] = '\0';
    printf("ACL: %s\n", aclValue);

    return 0;
}
