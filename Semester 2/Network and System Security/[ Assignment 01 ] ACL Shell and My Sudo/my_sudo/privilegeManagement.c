#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <errno.h>
#include <syslog.h>
#include <string.h>
#include "privilegeManagement.h"

void executeCommand(char *command[], uid_t targetUid) {
    pid_t pid = fork();
    if (pid < 0) {
        syslog(LOG_CRIT, "Fork failed: %s", strerror(errno));
        exit(EXIT_FAILURE);
    }

    if (pid == 0) { // Child process
        // Drop privileges to target user
        if (seteuid(targetUid) < 0 || setuid(targetUid) < 0) {
            syslog(LOG_CRIT, "UID transition failed");
            _exit(EXIT_FAILURE);
        }

        // Execute the command
        execvp(command[0], command);
        syslog(LOG_ERR, "execvp failed: %s", strerror(errno));
        _exit(EXIT_FAILURE);
    } else { // Parent process
        int status;
        waitpid(pid, &status, 0);
        if (WIFEXITED(status)) {
            syslog(LOG_INFO, "Command exited: %d", WEXITSTATUS(status));
        } else {
            syslog(LOG_WARNING, "Command terminated abnormally");
        }
    }
}

void dropPrivileges() {
    if (seteuid(getuid()) < 0) {
        syslog(LOG_CRIT, "Privilege cleanup failed");
    }
}
