#include <iostream>

void swap(int *a, int *b) {
    int temp = *a;
    *a = *b, *b = temp;
}

void insertStep (int arr[], int k) {
    if (k <= 0) return;

    if (arr[k] < arr[k  - 1]) {
        swap(arr+k, arr+k-1);
        insertStep(arr, k-1);
    }
    else return;
}

// // Method 1: insertionSort without recursive
// void insertionSort (int arr[], int aSize) {
//     for (int i = 0; i < aSize; i++)
//         insertStep(arr, i);
// }

// Method 2: insertionSort with recursive from starting
void insertionSort (int arr[], int aSize, int i) {
    if (i >= aSize)
        return;

    if (i < aSize) {
        insertStep(arr, i);
        insertionSort(arr, aSize, i+1);
    }
}

// Method 3: insertionSort with recursive from Ending
void insertionSort (int arr[], int k) {
    if (k <= 0)
        return;

    insertStep(arr, k);
    insertionSort(arr, k-1);
}

int main () {
    int aSize;
    std :: cout << "Enter the Size of Array: ";
    std :: cin >> aSize;

    int arr[aSize];
    std :: cout << "Enter Elements of the Arrays :" << std :: endl;
    for (int i = 0; i < aSize; i++)
        std :: cin >> arr[i];

    // insertionSort(arr, aSize);
    // insertionSort(arr, aSize, 0);
    insertionSort(arr, aSize-1);
    for (int i = 0; i< aSize; i++)
        std :: cout << arr[i] << " ";
    std :: cout << std :: endl;
    return 0;
}