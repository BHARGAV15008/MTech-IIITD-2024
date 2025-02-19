#include <iostream>
using namespace std;

bool searchElements(int arr[10][10], int element, int iRow, int iCol, int row, int col){
    if(iRow == row && iCol == col){
        if (arr[row][col] == element) return true;
        else return false;
    }

    int midROw = (iRow+row)/2;
    int midCol = (iCol+col)/2;
    if (iCol != col){
        if (arr[midROw][midCol] > element)
            return searchElements(arr, element, iRow, iCol, row, midCol);
        else if (arr[midROw][midCol] < element)
            return searchElements(arr, element, iRow, midCol+1, row, col);
        else return true;
    } else {
        if(arr[midROw][col] < element){
            return searchElements(arr, element, midROw+1, iCol, row, col);
        }
        else if (arr[midROw][col] > element)
            return searchElements(arr, element, iRow, iCol, midROw, col);
        else return true;
    }
} 

int main (){
    int n, m, element;

    cout << "How many row and column in your array: ";
    cin >> n >> m;
    int arr[19][10];

    cout << "Enter element in array: \n";
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            cin >> arr[i][j];

    cout << "Which element you want check : ";
    cin >> element;
    
    bool ret = searchElements(arr, element, 0, 0, n-1, m-1);
    cout << ret;
    
    return 0;
}