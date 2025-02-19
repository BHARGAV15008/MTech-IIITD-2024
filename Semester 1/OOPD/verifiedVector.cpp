#include<iostream>
#include <vector>
using namespace std;


int main (){
vector<int> array{0, 3, 5};
for (int i = 0; i < array.size(); i++) { // Loop 1
    array[i] = array[i] * 2;
}
for (int i = 0; i < array.size() - 1; i++) { // Loop 2
    array.at(i) = array.at(i + 1) + 1;
}

}