#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <syslog.h>
#include "signalHandling.h"

void handleSignal(int sig) {
    syslog(LOG_WARNING, "Signal %d received. Dropping privileges.", sig);
    if (seteuid(getuid()) < 0) {
        syslog(LOG_CRIT, "Failed to drop privileges on signal!");
    }
    closelog();
    _exit(EXIT_FAILURE);
}

void registerSignalHandlers() {
    signal(SIGINT, handleSignal);
    signal(SIGTERM, handleSignal);
}
