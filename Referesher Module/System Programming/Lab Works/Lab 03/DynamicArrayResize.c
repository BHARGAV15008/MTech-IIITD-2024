#include <stdio.h>
#include <stdlib.h>

int main() {
    int arrSize, newArrSize;
    int *arr;
    char yn;
    int i;

    printf("\nEnter the size of the array: ");
    scanf("%d", &arrSize);

    arr = (int *)malloc(arrSize * sizeof(int));
    if (arr == NULL) {
        printf("Memory allocation failed\n");
        return 1;
    }

    printf("\nEnter %d elements: ", arrSize);
    for (i = 0; i < arrSize; i++)
        scanf("%d", &arr[i]);

    printf("\nThe array elements are:");
    for (i = 0; i < arrSize; i++)
        printf(" %d", arr[i]);

    while (getchar() != '\n'); // for check yn not takes input

    printf("\nDo you want to resize the array? (y/n): ");
    scanf("%c", &yn);

    if (yn == 'y') {
        printf("\nEnter the new size of the array: ");
        scanf("%d", &newArrSize);

        arr = (int *)realloc(arr, newArrSize * sizeof(int));
        if (arr == NULL) {
            printf("Memory allocation failed\n");
            return 1;
        }

        if (newArrSize > arrSize) {
            printf("\nEnter %d more elements: ", newArrSize - arrSize);
            for (i = arrSize; i < newArrSize; i++)
                scanf("%d", &arr[i]);
        }

        arrSize = newArrSize;
        printf("\nThe array elements after resizing are:");
        for (i = 0; i < arrSize; i++)
            printf(" %d", arr[i]);
    }

    printf("\nReversing the array...");
    int temp;
    for (i = 0; i < arrSize / 2; i++) {
        temp = arr[arrSize - 1 - i];
        arr[arrSize - 1 - i] = arr[i];
        arr[i] = temp;
    }

    printf("\nThe array elements after reversing are:");
    for (i = 0; i < arrSize; i++)
        printf(" %d", arr[i]);

    printf("\nFreeing the memory and exiting the program...");
    free(arr);

    return 0;
}
