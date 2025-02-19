#include <iostream>
using namespace std;

// Copied Array...
void copyElement (int destArray[], int srcArray[], int destInd, int srcInd, int srcSize) {
    while (srcInd < srcSize) destArray[destInd++] = srcArray[srcInd++];
}

// Merging two array by using Recursive Approach...
void mergeSortedArrayRec (int resArr[], int arr1[], int arr2[], int size1, int size2, int init1, int init2) {
    static int k;
    if (size1 == init1){ copyElement (resArr, arr2, k, init2, size2); return; }
    if (size2 == init2){ copyElement (resArr, arr1, k, init1, size1); return; }

    if (init1 < size1 && init2 < size2) {
        if (arr1[init1] < arr2[init2]){ 
            resArr[k++] = arr1[init1++];
            mergeSortedArrayRec(resArr, arr1, arr2, size1, size2, init1, init2);
        } else {
            resArr[k++] = arr2[init2++];
            mergeSortedArrayRec(resArr, arr1, arr2, size1, size2, init1, init2);
        }
    }
}

// Merging two array by using Iteration Approach...
void mergeSortedArrayIter (int resArr[], int arr1[], int arr2[], int size1, int size2) {
    int k, i, j;
    k = i = j = 0;

    while (i < size1 && j < size2) {
        if (arr1[i] > arr2[j]) resArr[k++] = arr2[j++];
        else resArr[k++] = arr1[i++];
    }

    if (size1 == i){ copyElement (resArr, arr2, k, j, size2); return; }
    if (size2 == j){ copyElement (resArr, arr1, k, i, size1); return; }
}

// Display array...
void printArray (int arr[], int sizeArr) {
    for (int i = 0; i < sizeArr; i++) cout << arr[i] << "  ";
}

int main () {
    int sizeArr1, sizeArr2;
    cout << "Enter size of First Array: ";
    cin >> sizeArr1;

    int arr1[sizeArr1];
    cout << "Enter elements of Array: ";
    for (int i = 0; i < sizeArr1; i++) cin >> arr1[i];

    cout << "Enter size of Second Array: ";
    cin >> sizeArr2;

    int arr2[sizeArr2];
    cout << "Enter elements of Array: ";
    for (int i = 0; i < sizeArr2; i++) cin >> arr2[i];

    int resArr[sizeArr1+sizeArr2];

    // mergeSortedArrayRec (resArr, arr1, arr2, sizeArr1, sizeArr2, 0, 0); // Merge element using Recursive;
    mergeSortedArrayIter (resArr, arr1, arr2, sizeArr1, sizeArr2); // Merge element using Iterative;
    cout << "\n" << "Sorted Array : ";
    printArray (resArr, (sizeArr1+sizeArr2));
    
    return 0;
}