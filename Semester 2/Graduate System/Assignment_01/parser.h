#ifndef PARSER_H
#define PARSER_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_INPUT_SIZE 1024
#define MAX_ARGS 100

char* trim_whitespace(char* str);
char *read_input();
char **parse_input(char *input);

#endif