#include "shell.h"
#include "parser.h"
#include "execute.h"
#include "redir.h"
#include "prompt.h"

void visualize_process_tree() {
    system("ps -f");
}

int main() {
    char *input;
    char **args;
    char *cmd;
    int status;

    while (1) {
        display_prompt();
        input = read_input();
        args = parse_input(input);

        if (args[0] != NULL && strcmp(args[0], "exit") == 0) {
            free(input);
            free(args);
            break;
        }

        if (has_redirection(args)) {
            handle_redirection(args);
        } else {
            cmd = args[0];
            status = execute_command(cmd, args);
        }

        free(input);
        free(args);
        visualize_process_tree();
    }

    return 0;
}