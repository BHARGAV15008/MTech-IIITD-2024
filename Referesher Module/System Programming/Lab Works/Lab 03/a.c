#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int a[1000] = {};

int main() {
    srand(time(NULL));
    a[rand() % 1000] = 1;

    for (int i = 0; i < 1000; i++) {
        printf("%d\n", a[i]);
    }
}