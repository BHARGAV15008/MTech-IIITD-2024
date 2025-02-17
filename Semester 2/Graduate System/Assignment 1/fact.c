#include <stdio.h>
#include <stdlib.h>

int fact(int n) {
    if (n == 1 || n == 0)
        return 1;
    else
        return n * fact(n - 1);
}

int main(int argc, char *argv[]) {
    if (argc > 2){
        perror("Too many arguments you have passed!");
        return 1;
    } 
    else if (argc == 1) {
        perror("You have not passed any arguments!");
        return 1;
    }

    int num = atoi(argv[1]);
    if (num < 0) {
        perror("Factorial is not defined for negative numbers!");
        return 1;
    }

    printf("Factorial of %d is %d\n", num, fact(num));
    return 0;
}