#include <iostream>
using namespace std;

class MyClass {
	int x ;
	public :
		MyClass :: increment() { x *= 5 ; }
		MyClass :: MyClass(){
			x = 1;
		}

		MyClass :: MyClass ( MyClass &m) {
			x = m.x;
		}
};

int main ( void ) {
	MyClass m, n;
	m.increment();
	n = m;
	cout << m.x << " " << n.x;
	return 0 ;
}
