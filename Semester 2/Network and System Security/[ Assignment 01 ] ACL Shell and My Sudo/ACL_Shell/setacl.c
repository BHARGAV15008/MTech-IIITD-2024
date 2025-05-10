#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <pwd.h>
#include <unistd.h>
#ifdef __FreeBSD__
#include <sys/extattr.h>
#else
#include <sys/xattr.h>
#endif

int main(int argc, char *argv[]) {
    if (argc != 4) {
        fprintf(stderr, "Usage: setacl <file> <user> <permissions>\n");
        return 1;
    }

    const char *path = argv[1];
    const char *user = argv[2];
    const char *perms = argv[3];

    // Only the file owner can set ACLs
    struct stat st;
    if (stat(path, &st) < 0) {
        perror("stat");
        return 1;
    }

    // Allow either the file owner or root to set ACLs
    if (st.st_uid != getuid() && getuid() != 0) {
        fprintf(stderr, "Only the file owner or root can set ACLs\n");
        return 1;
    }

    // Set ACL
    char aclValue[256];
    snprintf(aclValue, sizeof(aclValue), "%s,%s", user, perms);

#ifdef __FreeBSD__
    // On FreeBSD, we need to use the USER namespace and the attribute name is just "acl"
    if (extattr_set_file(path, EXTATTR_NAMESPACE_USER, "acl", aclValue, strlen(aclValue)) < 0) {
        perror("extattr_set_file");
        return 1;
    }
#else
    if (setxattr(path, "user.acl", aclValue, strlen(aclValue), 0) < 0) {
        perror("setxattr");
        return 1;
    }
#endif

    printf("ACL set successfully for %s: %s,%s\n", path, user, perms);
    return 0;
}
