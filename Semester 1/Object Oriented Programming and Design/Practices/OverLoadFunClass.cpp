#include <iostream>
using namespace std;

class Base{
public:
    Base(){ cout << "Base Function Constructor" << endl; }
    void base(){ cout << "Base’s base()" << endl; }
};

class Derived : public Base{
public:
    // using Base::base;  // Bring base() from Base class into scope
    void base(int a){ cout << "Derived’s base(int)" << endl; }
};

int main(void){
    Derived* d = NULL;
    d = new Derived;

    d->base();  // Calls Base class base() function

    delete d;
    return 0;
}
