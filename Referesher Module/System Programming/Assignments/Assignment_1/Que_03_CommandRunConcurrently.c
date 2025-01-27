#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <unistd.h>

typedef struct {
    char* commands;
} Rcmd;

void runCommand(Rcmd *arg) {
    int id = fork();

    // ---------------  CASE I - For Windows  -------------------------------------
    
    if (id == 0 && system(arg->commands) == 0)
        printf("\nSystem successfully run: %s\n\n", arg->commands);

    // ---------------  CASE II - For Unix  -------------------------------------

    // if (_execl("/bin/sh", "sh", "-c", arg->commands, NULL) != -1)
    //     printf("\nSystem successfully run: %s\n\n", arg->commands);
}

void* call(void* arg) {
    runCommand((Rcmd*) arg);
    pthread_exit(NULL);
}

int main() {
    char *cmds[] = {"dir", "echo Hello_World", "mkdir newFolder", "rmdir newFolder"};
    int noCommands = sizeof(cmds)/sizeof(cmds[0]);
    pthread_t threads[noCommands];
    Rcmd command[noCommands];

    // Create threads
    for (int i = 0; i < noCommands; i++) {
        // Here we assigned command according threads:
        /*
            Thread 1: dir;
            Thread 2: echo 'Hello World';
            Thread 3: mkdir 'newFolder';
            Thread 4: rmdir 'newFolder';
        */
        

        command[i].commands = malloc(strlen(cmds[i]) + 1);  // Allocation

        strcpy(command[i].commands, cmds[i]);
        pthread_create(&threads[i], NULL, call, (void*) &command[i]);
        sleep(1);  // Take 1 second for showing output properly;
    }

    // Join threads
    for (int i = 0; i < noCommands; i++) {
        pthread_join(threads[i], NULL);
        free(command[i].commands);  // Deallocation
    }

    return 0;
}