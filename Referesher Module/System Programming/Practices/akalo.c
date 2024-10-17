#include <stdio.h>

// int* func(){
//     static int arr[5] = {1, 2, 10, 4, 5};
//     return arr;
// }
// int* func1(){
//     static int arr[5] = {11, 12, 110, 14, 15};
//     return arr;
// }

int main () {
    // //                  0       1
    // int* (*arr[2])() = {func, func1};
    // printf("%d", ((*arr[1])())[2]);

    int a[5] = {11, 12, 110, 14, 15};
    int *p, **q;
    p = a;
    *q = a;

    printf("a -> %d\n", a);             // base address of A
    printf("&a[0] -> %d\n", &a[0]);     // base address of A
    printf("p -> %d\n", p);             // base address of A
    printf("q -> %d\n", q);             // not return address of A
    printf("*p -> %d\n", *p);           // First value of A
    printf("*q -> %d\n", *q);           // Base adress of A
    // printf("**q -> %d\n", *(*q));         // Forst value of A
    return 0;
}