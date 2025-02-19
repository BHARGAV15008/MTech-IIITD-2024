#include <iostream>
#include <vector>
using namespace std;

vector<int> optSubArrayMinMax(int arr[], int n) {
    vector<int> chkLeft(n), chkRight(n), result(n, 0);

    for (int i = 0; i < n; i++)
        chkLeft[i] = (i - 1),
        chkRight[i] = (i + 1);

    for (int i = 0; i < n; i++)
        while (chkLeft[i] >= 0 && arr[chkLeft[i]] >= arr[i])
            chkLeft[i] = chkLeft[chkLeft[i]];

    for (int i = n - 1; i >= 0; i--)
        while (chkRight[i] < n && arr[chkRight[i]] >= arr[i])
            chkRight[i] = chkRight[chkRight[i]];

    for (int i = 0; i < n; i++) {
        int len = chkRight[i] - chkLeft[i] - 1;
        result[len - 1] = max(result[len - 1], arr[i]);
    }

    for (int i = n - 2; i >= 0; i--) 
        result[i] = max(result[i], result[i + 1]);

    return result;
}

int main() {
    int arr[] = {3, 1, 2, 4};
    int n = sizeof(arr) / sizeof(arr[0]);

    vector<int> result = optSubArrayMinMax(arr, n);

    cout << "Resulting array: ";
    for (int i = 0; i < n; i++) 
        cout << result[i] << " ";
    cout << endl;

    return 0;
}
