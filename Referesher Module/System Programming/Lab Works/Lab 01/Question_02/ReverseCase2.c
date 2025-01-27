#include <stdio.h>
#include <string.h>
#include <ctype.h>

void reverseCase(char* str) {
    int i = 0;
    while(str[i] != '\0') {
        if(islower(str[i]))
            str[i] = toupper(str[i]);
        else if(isupper(str[i]))
            str[i] = tolower(str[i]);
        i++;
    }
}

int main() {
    char str[20];
    scanf("%[^\n]s", &str);
    reverseCase(str);
    puts(str);
    return 0;
}

