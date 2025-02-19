#include <iostream>
#include <vector>
using namespace std;

void swap(int &a, int &b)
{
    int temp = a;
    a = b;
    b = temp;
}

int partition(vector<int> &A, vector<int> &B, int l1, int h2, int kth)
{
    int i = l1, j = h2;
    int n = A.size();
    int pivot;

    if (kth < n)
        pivot = A[kth];
    else
        pivot = B[kth - n];

    if (kth < n)
        swap(A[kth], A[l1]);
    else
        swap(B[kth - n], (l1 < n) ? A[l1] : B[l1 - n]);

    while (i <= j)
    {
        while (i <= h2 && (i < n ? A[i] : B[i - n]) <= pivot)
            i++;

        while (j >= l1 && (j < n ? A[j] : B[j - n]) > pivot)
            j--;

        if (i < j)
        {
            if (i < n && j < n)
                swap(A[i], A[j]);
            else if (i < n && j >= n)
                swap(A[i], B[j - n]);
            else
                swap(B[i - n], B[j - n]);
        }
    }

    if (l1 < n && j < n)
        swap(A[l1], A[j]);
    else if (l1 < n)
        swap(A[l1], B[j - n]);
    else
        swap(B[l1 - n], B[j - n]);

    return j;
}

int median(vector<int> &A, vector<int> &B, int l1, int h2, int kth)
{
    int n = A.size();
    int pivot = partition(A, B, l1, h2, l1);
    cout << pivot << " " << (pivot < n ? A[pivot] : B[pivot - n]) << "\n ";

    if (pivot > kth)
        return median(A, B, l1, pivot - 1, kth);
    else if (pivot < kth)
        return median(A, B, pivot + 1, h2, kth);
    else
    {
        if (kth >= n)
            return B[kth - n];
        else
            return A[kth];
    }
}

int main()
{
    vector<int> A = {-10, -5, 0, 5, 10};
    vector<int> B = {-15, -20, 15, 20, 25};
    cout << median(A, B, 0, 9, (A.size() + B.size()) / 2 - 1);

    return 0;
}