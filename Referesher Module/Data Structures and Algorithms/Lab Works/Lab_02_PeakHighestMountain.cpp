#include <iostream>
using namespace std;

int peakHighestMountainFromNeighbour(int mou[], int init, int size) {
    int mid1 = size/2;
    int mid2 = size/2;

    int ret = 0;

    while (mid1 >= init || mid2 >= size-2){
        if(mid1 >= init){
            if(mou[mid1] > mou[mid1+1] && mou[mid1] > mou[mid1-1]) return init;
            else mid1 = (mid1+init)/2;
        } else {
            if(mou[mid2] > mou[mid2+1] && mou[mid2] > mou[mid2-1]) return init;
            else mid2 = (mid2+size-2)/2;
        }
    }
    
    return 0; 
}

int main (){
    int mountains[] = {1, 3, 20, 4, 5, 6, 7, 3, 2};
    int size = sizeof(mountains)/sizeof(int);
    int peak = peakHighestMountainFromNeighbour(mountains, 2, size);
    if(peak == 0)
        cout << "Peak Mountain not found...";
    else cout << peak;
    
    return 0;
}   