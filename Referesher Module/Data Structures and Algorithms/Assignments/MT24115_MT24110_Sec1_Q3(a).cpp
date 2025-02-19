#include <iostream>
#include <vector>
using namespace std;

vector<int> subArrayMinMax(int arr[], int n) {
    vector<int> result(n, 0);

    for (int size = 1; size <= n; size++) {
        int maxOfMin = INT_MIN;
        for (int i = 0; i < n - size + 1; i++) {
            int subArrMin = INT_MAX;
            for (int j = i; j < i + size; j++)
                subArrMin = min(subArrMin, arr[j]);

            maxOfMin = max(maxOfMin, subArrMin);
        }
        result[size - 1] = maxOfMin;
    }

    return result;
}

int main() {
    int arr[] = {3, 1, 2, 4};
    int n = sizeof(arr) / sizeof(arr[0]);

    vector<int> result = subArrayMinMax(arr, n);

    cout << "resulting array: ";
    for (int i = 0; i < n; i++) 
        cout << result[i] << " ";
    cout << endl;
    return 0;
}