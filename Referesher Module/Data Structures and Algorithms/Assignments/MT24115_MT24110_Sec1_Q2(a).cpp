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

int recMergeSort(int arr[], int low, int high){
    int mid;
    if(low < high){
        mid = (low + high) / 2;
        recMergeSort(arr, low, mid);
        recMergeSort(arr, mid + 1, high);
        combineArray(arr, low, mid, high);
    }

    set<int> s(arr, arr+high+1);
    int i = 0;
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
    
    
    size = recMergeSort(arr, 0, size-1);
    // Displaying Sorted Array;
    cout << "Dispaying sorted array: \n";
    for(int i = 0; i < size; i++)
        cout << arr[i] << " ";

    
    return 0;
}