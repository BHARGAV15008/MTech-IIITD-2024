#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <pwd.h>
#include <unistd.h>
#include <sys/extattr.h> // FreeBSD specific

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: setacl <file> <user,permissions>\n");
        fprintf(stderr, "Example: setacl example.txt user1,rw\n");
        return 1;
    }

    const char *path = argv[1];
    const char *acl_entry = argv[2];

    // Validate the ACL entry format
    if (strchr(acl_entry, ',') == NULL) {
        fprintf(stderr, "Invalid ACL format. Use: user,permissions\n");
        fprintf(stderr, "Example: user1,rw\n");
        return 1;
    }

    // Only the file owner can set ACLs
    struct stat st;
    if (stat(path, &st) < 0) {
        perror("stat");
        return 1;
    }

    if (st.st_uid != getuid()) {
        fprintf(stderr, "Only the file owner can set ACLs\n");
        return 1;
    }

    // Read existing ACL if any
    char existing_acl[1024] = "";
    ssize_t len = extattr_get_file(path, EXTATTR_NAMESPACE_USER, "user.acl",
                                   existing_acl, sizeof(existing_acl) - 1);

    // Parse user from the new ACL entry
    char acl_copy[256];
    strncpy(acl_copy, acl_entry, sizeof(acl_copy) - 1);
    acl_copy[sizeof(acl_copy) - 1] = '\0';

    char *comma = strchr(acl_copy, ',');
    *comma = '\0';
    const char *new_user = acl_copy;

    // Prepare the new ACL value
    char new_acl[1024];
    if (len > 0) {
        existing_acl[len] = '\0';

        // Check if this user already has an entry
        char *user_entry = strstr(existing_acl, new_user);
        if (user_entry != NULL &&
            (user_entry == existing_acl || *(user_entry - 1) == ' ') &&
            *(user_entry + strlen(new_user)) == ',') {

            // Replace existing entry
            char *entry_end = strchr(user_entry, ' ');
            if (entry_end == NULL) entry_end = user_entry + strlen(user_entry);

            size_t prefix_len = user_entry - existing_acl;
            char prefix[1024] = "";
            if (prefix_len > 0) {
                strncpy(prefix, existing_acl, prefix_len);
                prefix[prefix_len] = '\0';
            }

            if (*entry_end == ' ') {
                snprintf(new_acl, sizeof(new_acl), "%s%s%s",
                         prefix, acl_entry, entry_end);
            } else {
                snprintf(new_acl, sizeof(new_acl), "%s%s",
                         prefix, acl_entry);
            }
        } else {
            // Add new entry
            snprintf(new_acl, sizeof(new_acl), "%s %s",
                     existing_acl, acl_entry);
        }
    } else {
        // No existing ACL, just use the new entry
        strncpy(new_acl, acl_entry, sizeof(new_acl) - 1);
        new_acl[sizeof(new_acl) - 1] = '\0';
    }

    // Set the ACL
    if (extattr_set_file(path, EXTATTR_NAMESPACE_USER, "user.acl",
                         new_acl, strlen(new_acl)) < 0) {
        perror("extattr_set_file");
        return 1;
    }

    printf("ACL set successfully: %s\n", new_acl);
    return 0;
}
