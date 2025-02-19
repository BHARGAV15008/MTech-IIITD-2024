#include <iostream>
#include <set>
using namespace std;

void combineArray(int arr[], int low, int mid, int high){
    int i = low, j = mid + 1, k = low;
    int newArr[10];
    while (i <= mid && j <= high){
        if (arr[i] <= arr[j]) newArr[k++] = arr[i++];
        else newArr[k++] = arr[j++];
    }

    while (i <= mid) newArr[k++] = arr[i++];
        
    while (j <= high) newArr[k++] = arr[j++];

    for (int i = low; i <= high; i++) arr[i] = newArr[i];
}

int iterMergeSort(int arr[], int size) {
    int i = 1 /* Here 'i' defined size of the array initially where we sorting. */, 
    start /*Here 'start' defined starting point.*/,
    middle /*Finding middle elements.*/,
    end /*Here it define traversal until.*/;
    while (i <= size) {
        start = 0;
        while (start < size) {
            middle = (start+i-1 < size) ? (start+i-1) : size;
            end = (start+2*i-1 < size) ? (start+2*i-1) : size;
            combineArray(arr, start, middle, end);

            start += 2*i;
        }
        i *= 2;
    }

    set<int> s(arr, arr+size+1);
    i = 0;
    for (int value : s) {
        arr[i++] = value;
    }
    return s.size();
}

int main (){
    int size;

    cout << "Number of elements: ";
    cin >> size;
    int arr[size];

    cout << "Enter your Elements: \n";
    for(int i = 0; i < size; i++)
        cin >> arr[i];
    
    
    size = iterMergeSort(arr, size-1);
    // Displaying Sorted Array;
    cout << "Dispaying sorted array: \n";
    for(int i = 0; i < size; i++)
        cout << arr[i] << " ";

    
    return 0;
}