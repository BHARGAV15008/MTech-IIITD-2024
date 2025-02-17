#include <iostream>
using namespace std;

// Here we define two sort guest method for ARJUN'S method and PRIYA's method
void sortGuest (int arr[], int low, int high, int p);
void sortGuest (int arr[], int low, int high, float a);
void swapGuest (int &a, int &b);
int theClimaxPivot(int arr[], int low, int high);   // Priya's method;
int theOpeningScenePivot(int arr[], int low, int high);   // Arjun's method;

int main (){
    // for indication
    int priya = 1;
    float arjun = 1.0;

    int ng; // define no. of guest;
    // Here we take input of the incomming guest ID;
    cout << "Number of guest: ";
    cin >> ng;

    int guest[ng];  // Listing guest by their id;
    cout << "Enter guest ids: ";
    for (int i = 0; i < ng; i++)
        cin >> guest[i];

    sortGuest(guest, 0, ng-1, priya);
    for (int i = 0; i < ng; i++)
        cout << guest[i] << "  ";

    // sortGuest(guest, 0, ng-1, arjun);
    // for (int i = 0; i < ng; i++)
        // cout << guest[i] << "  ";
    
    return 0;
}

void swapGuest (int &a, int &b) {
    int temp = a;
    a = b;
    b = temp;
}

void sortGuest (int arr[], int low, int high, int p) {
    int pvt;
    if (low < high) {
        pvt = theClimaxPivot(arr, low, high);
        sortGuest(arr, low, pvt - 1, p);
        sortGuest(arr, pvt + 1, high, p);
    }
}

void sortGuest (int arr[], int low, int high, float a) {
    int pvt;
    if (low < high) {
        pvt = theOpeningScenePivot(arr, low, high);
        sortGuest(arr, low, pvt - 1, a);
        sortGuest(arr, pvt + 1, high, a);
    }
}

int theClimaxPivot(int arr[], int low, int high) {
    // Here we consider last element as a climax pivot;
    int pvt = arr[high];
    int i = low - 1;

    for (int j = low; j < high; j++) {
        if (arr[j] <= pvt) {
            i++;
            swapGuest(*(arr+i), *(arr+j));
        }
    }
    swapGuest(*(arr+i + 1), *(arr+high));
    return i + 1;
}

int theOpeningScenePivot(int arr[], int low, int high) {
    // Here we consider first element as a openingScene pivot;
    int pvt = arr[low];
    int i = high + 1;

    for (int j = high; j > low; j--) {
        if (arr[j] > pvt) {
            i--;
            swapGuest(*(arr+i), *(arr+j));
        }
    }
    swapGuest(*(arr+i-1), *(arr+low));
    return i - 1;
}