#ifndef EXECUTE_H
#define EXECUTE_H

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/wait.h>

int execute_command(char *cmd, char **args);
void ls_command(char **args);
void help_command(char **args);

#endif