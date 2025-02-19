#include <iostream>
#include <vector>
using namespace std;

int recursiveClimbApproach(int steps){
    if (steps == 0) return 0;
    if (steps == 1) return 1;
    if (steps == 2) return 2;

    return recursiveClimbApproach(steps-1) + recursiveClimbApproach(steps-2);
}

int extraSpaceClimbApproach(int steps, int arr[]){
    int st = 0;
    if (steps == 0) arr[st] = 0;
    if (steps == 1) arr[st] = 1;
    if (steps == 2) arr[st] = 2;
    else {
        arr[st++] = 1, arr[st++] = 1;
        while (st <= steps)
            arr[st] = arr[st-1] + arr[st-2], st++;
    }
    return arr[st-1];
}

int optimalClimbApproach(int steps){
    int st = 2, final;
    if (steps == 0) return 0;
    if (steps == 1) return 1;
    if (steps == 2) return 2;
    else {
        int first = 1, second = 1;
        while (st <= steps)
            final = first+second, first = second, second = final, st++;
    }
    return final;
}

int main (){
    int arr[10];
    cout << optimalClimbApproach(3);
    
    return 0;
}