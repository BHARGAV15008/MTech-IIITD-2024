#include "logger.h"
#include "config.h"

void logMessage(const char *message) {
    FILE *logFile = fopen(LOG_FILE, "a");
    if (logFile == NULL) {
        perror("Failed to open log file");
        return;
    }

    time_t now = time(NULL);
    fprintf(logFile, "[%s] %s\n", ctime(&now), message);
    fclose(logFile);
}