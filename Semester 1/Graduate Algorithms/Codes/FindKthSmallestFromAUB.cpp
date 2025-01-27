#include <iostream>
#include <vector>
using namespace std;

void swap(int &a, int &b)
{
    int temp = a;
    a = b;
    b = temp;
}

// int partition(vector<int> &A, vector<int> &B, int l1, int l2, int h1, int h2, int kth)
// {
//     int i = l1, j = h2;
//     int n = A.size();
//     int pivot;

//     if (kth < n)
//         pivot = A[kth];
//     else
//         pivot = B[kth - n];

//     swap((kth < n ? A[kth] : B[kth - n]), (l1 < n ? A[l1] : B[l1 - n]));

//     while (i < j)
//     {
//         while ((i < n ? A[i] : B[i - n]) <= pivot && i <= h2 - 1)
//             i++;

//         while ((j < n ? A[j] : B[j - n]) > pivot && j >= l1 + 1)
//             j--;

//         if (i < j)
//             swap((i < n ? A[i] : B[i - n]), (j < n ? A[j] : B[j - n]));
//     }

//     // for (int j = l1; j < h2; ++j)
//     // {
//     //     if ((j < n ? A[j] : B[j - n]) < pivot)
//     //     {
//     //         i++;
//     //         swap((j < n ? A[j] : B[j - n]), (j < n ? A[j] : B[j - n]));
//     //     }
//     // }

//     if (j > n)
//         swap(B[j - n], kth < n ? A[kth] : B[kth - n]);
//     else
//         swap(A[j], kth < n ? A[kth] : B[kth - n]);

//     return j;
// }

// Partition function
int partition(vector<int> &A, vector<int> &B, int l1, int h2, int kth)
{
    int i = l1, j = h2;
    int n = A.size();
    int pivot;

    if (kth < n)
        pivot = A[kth];
    else
        pivot = B[kth - n];

    // Move pivot to the start
    if (kth < n)
        swap(A[kth], A[l1]);
    else
        swap(B[kth - n], (l1 < n) ? A[l1] : B[l1 - n]);

    // Adjust pivot position
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

    // Place pivot in its correct position
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
    // 0 1 2 3 5 6 7 8 9 10
    // cout << median(A, B, 0, 9, 4);
    cout << median(A, B, 0, 9, (A.size() + B.size()) / 2);
    // cout << partition(A, B, 0, 0, 4, 9, 0) << endl;
    // for (int i = 0; i < A.size(); i++)
    //     cout << A[i] << " ";
    // cout << endl;
    // for (int i = 0; i < A.size(); i++)
    //     cout << B[i] << " ";
    // cout << endl;
    // cout << partition(A, B, 0, 0, 4, 9, 1) << endl;
    // for (int i = 0; i < A.size(); i++)
    //     cout << A[i] << " ";
    // cout << endl;
    // for (int i = 0; i < A.size(); i++)
    //     cout << B[i] << " ";
    // cout << endl;
    // cout << partition(A, B, 0, 0, 4, 9, 2) << endl;
    // for (int i = 0; i < A.size(); i++)
    //     cout << A[i] << " ";
    // cout << endl;
    // for (int i = 0; i < A.size(); i++)
    //     cout << B[i] << " ";
    // cout << endl;
    // cout << partition(A, B, 0, 0, 4, 9, 3) << endl;
    // for (int i = 0; i < A.size(); i++)
    //     cout << A[i] << " ";
    // cout << endl;
    // for (int i = 0; i < A.size(); i++)
    //     cout << B[i] << " ";
    // cout << endl;
    // cout << partition(A, B, 0, 0, 4, 9, 4) << endl;
    // for (int i = 0; i < A.size(); i++)
    //     cout << A[i] << " ";
    // cout << endl;
    // for (int i = 0; i < A.size(); i++)
    //     cout << B[i] << " ";
    // cout << endl;
    // cout << partition(A, B, 0, 0, 4, 9, 5) << endl;
    // for (int i = 0; i < A.size(); i++)
    //     cout << A[i] << " ";
    // cout << endl;
    // for (int i = 0; i < A.size(); i++)
    //     cout << B[i] << " ";
    // cout << endl;
    // cout << partition(A, B, 0, 0, 4, 9, 6) << endl;
    // for (int i = 0; i < A.size(); i++)
    //     cout << A[i] << " ";
    // cout << endl;
    // for (int i = 0; i < A.size(); i++)
    //     cout << B[i] << " ";
    // cout << endl;
    // cout << partition(A, B, 0, 0, 4, 9, 7) << endl;
    // for (int i = 0; i < A.size(); i++)
    //     cout << A[i] << " ";
    // cout << endl;
    // for (int i = 0; i < A.size(); i++)
    //     cout << B[i] << " ";
    // cout << endl;

    return 0;
}

// #include <iostream>
// #include <vector>
// #include <cstdlib>
// using namespace std;

// // Function to swap elements
// void swap(int &a, int &b)
// {
//     int temp = a;
//     a = b;
//     b = temp;
// }

// // Partition function
// int partition(vector<int> &A, vector<int> &B, int l1, int l2, int h1, int h2, int kth)
// {
//     int i = l1, j = h2;
//     int n = A.size();
//     int pivot;

//     if (kth < n)
//         pivot = A[kth];
//     else
//         pivot = B[kth - n];

//     // Move pivot to the start
//     if (kth < n)
//         swap(A[kth], A[l1]);
//     else
//         swap(B[kth - n], (l1 < n) ? A[l1] : B[l1 - n]);

//     // Adjust pivot position
//     while (i <= j)
//     {
//         while (i <= h2 && (i < n ? A[i] : B[i - n]) <= pivot)
//             i++;

//         while (j >= l1 && (j < n ? A[j] : B[j - n]) > pivot)
//             j--;

//         if (i < j)
//         {
//             if (i < n && j < n)
//                 swap(A[i], A[j]);
//             else if (i < n && j >= n)
//                 swap(A[i], B[j - n]);
//             else
//                 swap(B[i - n], B[j - n]);
//         }
//     }

//     // Place pivot in its correct position
//     if (l1 < n && j < n)
//         swap(A[l1], A[j]);
//     else if (l1 < n)
//         swap(A[l1], B[j - n]);
//     else
//         swap(B[l1 - n], B[j - n]);

//     return j;
// }

// int main()
// {
// vector<int> A = {-10, -5, 0, 5, 10};
// vector<int> B = {-15, -20, 15, 20, 25};
//     cout << "Initial vectors:" << endl;
//     for (int x : A)
//         cout << x << " ";
//     cout << endl;
//     for (int x : B)
//         cout << x << " ";
//     cout << endl;

//     int kth = 0; // Example kth index
//     int pivot_index = partition(A, B, 0, 0, 4, 9, kth);

//     cout << "After partition with pivot index " << pivot_index << ":" << endl;
//     for (int x : A)
//         cout << x << " ";
//     cout << endl;
//     for (int x : B)
//         cout << x << " ";
//     cout << endl;

//     return 0;
// }
