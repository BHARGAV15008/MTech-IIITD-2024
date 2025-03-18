#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

// Helper function to generate ACL file path
static char* get_acl_file_path(const char* path) {
    size_t len = strlen(path);
    char* acl_path = malloc(len + 5); // path + ".acl" + null terminator

    if (!acl_path) {
        perror("malloc");
        return NULL;
    }

    sprintf(acl_path, "%s.acl", path);
    return acl_path;
}

int checkAcl(const char *path, const char *user, char mode) {
    // Generate ACL file path
    char* acl_path = get_acl_file_path(path);
    if (!acl_path) {
        return 0; // Error, fall back to DAC permissions
    }

    // Open the ACL file
    FILE* acl_file = fopen(acl_path, "r");
    if (!acl_file) {
        // If file doesn't exist, fall back to DAC permissions
        if (errno == ENOENT) {
            printf("No ACL file found for path: %s (falling back to DAC)\n", path);
            free(acl_path);
            return 0;
        }

        perror("fopen");
        free(acl_path);
        return 0;
    }

    free(acl_path); // Free the path since we don't need it anymore

    // Read the ACL file
    char aclValue[1024];
    if (!fgets(aclValue, sizeof(aclValue), acl_file)) {
        // Empty or unreadable file
        fclose(acl_file);
        return 0;
    }

    fclose(acl_file);

    // Remove newline character if present
    size_t len = strlen(aclValue);
    if (len > 0 && aclValue[len-1] == '\n') {
        aclValue[len-1] = '\0';
    }

    printf("Retrieved ACL: %s\n", aclValue);

    // Tokenize the ACL string by spaces
    char* aclCopy = strdup(aclValue);
    if (!aclCopy) {
        perror("strdup");
        return 0;
    }

    char* saveptr;
    char* token = strtok_r(aclCopy, " ", &saveptr);

    while (token != NULL) {
        // Split the token into username and permissions
        char* comma = strchr(token, ',');
        if (!comma) {
            token = strtok_r(NULL, " ", &saveptr);
            continue;
        }

        *comma = '\0'; // Split the token into username and permissions
        if (strcmp(token, user) == 0) {
            if (strchr(comma + 1, mode) != NULL) {
                printf("ACL allows access for user: %s\n", user);
                free(aclCopy);
                return 1; // ACL allows access
            }
        }

        token = strtok_r(NULL, " ", &saveptr);
    }

    free(aclCopy);
    printf("ACL denies access for user: %s\n", user);
    return 0; // ACL denies access
}

// Function to set ACL for a file
int setAcl(const char *path, const char *acl_entry) {
    // Generate ACL file path
    char* acl_path = get_acl_file_path(path);
    if (!acl_path) {
        return -1; // Error
    }

    // Check if the ACL file already exists
    FILE* acl_file = fopen(acl_path, "r");
    char existing_acl[1024] = "";

    if (acl_file) {
        // Read existing ACL
        if (fgets(existing_acl, sizeof(existing_acl), acl_file)) {
            // Remove newline character if present
            size_t len = strlen(existing_acl);
            if (len > 0 && existing_acl[len-1] == '\n') {
                existing_acl[len-1] = '\0';
            }
        }
        fclose(acl_file);
    }

    // Parse user from the new ACL entry
    char acl_copy[256];
    strncpy(acl_copy, acl_entry, sizeof(acl_copy) - 1);
    acl_copy[sizeof(acl_copy) - 1] = '\0';

    char* comma = strchr(acl_copy, ',');
    if (!comma) {
        free(acl_path);
        return -1; // Invalid format
    }

    *comma = '\0';
    const char* new_user = acl_copy;

    // Prepare the new ACL value
    char new_acl[1024];
    if (strlen(existing_acl) > 0) {
        // Check if this user already has an entry
        char* user_entry = strstr(existing_acl, new_user);
        if (user_entry != NULL &&
            (user_entry == existing_acl || *(user_entry - 1) == ' ') &&
            *(user_entry + strlen(new_user)) == ',') {

            // Replace existing entry
            char* entry_end = strchr(user_entry, ' ');
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

    // Write the new ACL
    acl_file = fopen(acl_path, "w");
    if (!acl_file) {
        perror("fopen");
        free(acl_path);
        return -1;
    }

    fprintf(acl_file, "%s\n", new_acl);
    fclose(acl_file);

    // Set the ACL file to be hidden (mode 0600)
    chmod(acl_path, 0600);

    free(acl_path);
    return 0;
}

// Function to get ACL for a file
int getAcl(const char *path, char *acl_buffer, size_t buffer_size) {
    // Generate ACL file path
    char* acl_path = get_acl_file_path(path);
    if (!acl_path) {
        return -1; // Error
    }

    // Open the ACL file
    FILE* acl_file = fopen(acl_path, "r");
    if (!acl_file) {
        // If file doesn't exist, no ACL is set
        if (errno == ENOENT) {
            snprintf(acl_buffer, buffer_size, "No ACL set for file: %s", path);
            free(acl_path);
            return 0;
        }

        perror("fopen");
        free(acl_path);
        return -1;
    }

    // Read the ACL
    if (!fgets(acl_buffer, buffer_size, acl_file)) {
        // Empty file
        snprintf(acl_buffer, buffer_size, "No ACL set for file: %s", path);
        fclose(acl_file);
        free(acl_path);
        return 0;
    }

    fclose(acl_file);
    free(acl_path);

    // Remove newline character if present
    size_t len = strlen(acl_buffer);
    if (len > 0 && acl_buffer[len-1] == '\n') {
        acl_buffer[len-1] = '\0';
    }

    return 0;
}
