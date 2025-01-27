#include "prompt.h"

void display_prompt() {
    char hostname[1024];
    if (gethostname(hostname, sizeof(hostname)) == -1) {
        perror("gethostname failed");
        return;
    }

    char *user = getenv("USER");
    if (!user) {
        user = "unknown";
    }

    char cwd[1024];
    if (getcwd(cwd, sizeof(cwd)) == NULL) {
        perror("getcwd failed");
        return;
    }

    char prompt_symbol = '$';
    if (geteuid() == 0) {
        prompt_symbol = '#';
    }

    printf("\033[1;31m|-----\033[0m\033[1;32m[%s@%s]\033[0m\033[1;33m-----[%s]\033[0m\n", 
           user, hostname, cwd);

    printf("\033[1;36m|-----\033[0m\033[1;32m%c\033[0m\t", prompt_symbol);
}