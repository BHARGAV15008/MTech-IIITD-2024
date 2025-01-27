#ifndef REDIR_H
#define REDIR_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

int has_redirection(char **args);
void handle_redirection(char **args);

#endif