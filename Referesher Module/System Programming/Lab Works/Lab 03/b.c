#include <stdio.h>
#include <stdlib.h>

int a[1000] = {};

int main() {
    for (int i = 0; i < 1000; i++) {
        printf("%d\n", a[i]);
    }
}