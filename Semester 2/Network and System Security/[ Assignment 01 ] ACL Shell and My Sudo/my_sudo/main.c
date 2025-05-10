#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <syslog.h>
#include "pathValidation.h"
#include "privilegeManagement.h"
#include "signalHandling.h"

int main(int argc, char *argv[]) {
    openlog("my_sudo", LOG_PID | LOG_CONS, LOG_AUTH);

    // Register signal handlers
    registerSignalHandlers();

    // Argument validation
    if (argc < 2) {
        syslog(LOG_ERR, "Invalid arguments");
        fprintf(stderr, "Usage: %s <command> [args...]\n", argv[0]);
        closelog();
        exit(EXIT_FAILURE);
    }

    // Privilege verification
    if (geteuid() != 0) {
        syslog(LOG_ALERT, "Security violation: Non-root EUID");
        fprintf(stderr, "Program must be setuid root\n");
        closelog();
        exit(EXIT_FAILURE);
    }

    // Path security validation
    char *safePath = resolveSecurePath(argv[1]);
    if (!safePath) {
        syslog(LOG_ERR, "Path validation failed");
        closelog();
        exit(EXIT_FAILURE);
    }

    // Get target UID from file owner
    uid_t targetUid = getFileOwnerUid(safePath);
    free(safePath);

    // Execute command with security context
    executeCommand(&argv[1], targetUid);

    // Post-execution cleanup
    dropPrivileges();

    closelog();
    return EXIT_SUCCESS;
}
