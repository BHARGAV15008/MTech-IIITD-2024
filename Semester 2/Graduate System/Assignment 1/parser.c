#include "parser.h"

char* trim_whitespace(char* str) {
    while (isspace((unsigned char)*str)) str++;
    if (*str == 0)
        return str;
    char* end = str + strlen(str) - 1;
    while (end > str && isspace((unsigned char)*end)) end--;
    *(end + 1) = 0;
    return str;
}

char *read_input() {
    char *input = malloc(MAX_INPUT_SIZE);
    if (!input) {
        perror("malloc failed");
        exit(1);
    }

    if (fgets(input, MAX_INPUT_SIZE, stdin) == NULL) {
        perror("fgets failed");
        free(input);
        exit(1);
    }

    input[strcspn(input, "\n")] = 0;

    return input;
}

char **parse_input(char *input) {
    char **args = malloc(MAX_ARGS * sizeof(char *));
    if (!args) {
        perror("malloc failed");
        exit(1);
    }

    int i = 0;
    char *token = strtok(input, " ");
    
    while (token != NULL) {
        if (token[0] == '"') {
            token = &token[1];
            char *end_quote = strchr(token, '"');
            if (end_quote) {
                *end_quote = '\0';
            }
        } else if (token[0] == '\'') {
            token = &token[1];
            char *end_quote = strchr(token, '\'');
            if (end_quote) {
                *end_quote = '\0';
            }
        }

        args[i] = trim_whitespace(token);
        i++;
        token = strtok(NULL, " ");
    }

    args[i] = NULL;

    return args;
}