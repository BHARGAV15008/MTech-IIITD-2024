#include <iostream>
#include <vector>

void merge(std::vector<int> &vecs, int low, int mid, int high) {
       std::vector<int> upVecs(high - low + 1);
       int l = low, m = mid + 1, k = 0;
       
       while (l <= mid && m <= high) {
           if (vecs[l] <= vecs[m]) {
               upVecs[k++] = vecs[l++];
           } else {
               upVecs[k++] = vecs[m++];
           }
       }
       
       while (l <= mid) upVecs[k++] = vecs[l++];
       while (m <= high) upVecs[k++] = vecs[m++];
       
       std::copy(upVecs.begin(), upVecs.end(), vecs.begin() + low);
   }

void mergeSort (std :: vector<int> &vecs, int low, int high) {
    int mid;
    if (low < high) {
        mid = (low + high) / 2;
        mergeSort(vecs, low, mid);
        mergeSort(vecs, mid + 1, high);
        merge(vecs, low, mid, high);
    }
}

int main () {
    int aSize;
    std :: cout << "Enter the Size of Array: ";
    std :: cin >> aSize;

    std :: vector<int> vecs;
    std :: cout << "Enter Elements of the Arrays :" << std :: endl;
    int val;
    for (int i = 0; i < aSize; i++) {
        std :: cin >> val;
        vecs.push_back(val);
    }


    // insertionSort(arr, aSize);
    mergeSort(vecs, 0, vecs.size() - 1);
    for (int i = 0; i < vecs.size(); i++)
        std :: cout << vecs[i] << " ";
    std :: cout << std :: endl;
    return 0;
}