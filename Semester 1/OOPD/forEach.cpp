#include <iostream>
using namespace std;

int main() {
    int array[] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    
    // Range-based for loop to print elements
    // for (auto iter : array) {
    //    cout << iter << " ";  // No need to dereference iter, just use it directly
    // }

    for (auto iter = begin(array); iter != end(array); ++iter) {
        cout << *iter << " ";  // Dereferencing iter since it's a pointer
    }

    
    return 0;

}
