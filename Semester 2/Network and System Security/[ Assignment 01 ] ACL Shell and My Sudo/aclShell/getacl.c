    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include <errno.h>      // Add this line
    #include <sys/extattr.h> // FreeBSD specific

    int main(int argc, char *argv[]) {
        if (argc != 2) {
            fprintf(stderr, "Usage: getacl <file>\n");
            return 1;
        }

        const char *path = argv[1];

        // Get ACL
        char aclValue[256];
        ssize_t len;

        len = extattr_get_file(path, EXTATTR_NAMESPACE_USER, "user.acl", aclValue, sizeof(aclValue) - 1);

        if (len < 0) {
            if (errno == ENOATTR) {
                printf("No ACL set for file: %s\n", path);
                return 0;
            }
            perror("extattr_get_file");
            return 1;
        }

        aclValue[len] = '\0';
        printf("ACL for %s: %s\n", path, aclValue);

        return 0;
    }
