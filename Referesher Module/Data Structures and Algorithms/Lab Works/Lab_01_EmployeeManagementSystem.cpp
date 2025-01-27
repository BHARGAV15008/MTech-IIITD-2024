#include <iostream>
#include <string>
using namespace std;

class Employee{
    int id;
    float salary;
    string name;

    public:
        Employee(int id, float salary, string name){
            this->id = id;
            this->salary = salary;
            this->name = name;
        }

        float getSalary() {
            return salary;
        }

        int getId() {
            return id;
        }

        string getName() {
            return name;
        }
};

void swapEmployee (Employee *emp1, Employee *emp2){
    Employee temp = *emp1;
    *emp1 = *emp2;
    *emp2 = temp;
}

void sort_employees_by_salary(Employee emp[], int size){
    // Sorting Employee according their salary by using insertionSort
    int j;
    for(int i = 1; i < size; i++){
        Employee insert = emp[i];
        j = i-1;
        while(insert.getSalary() < emp[j].getSalary() && j >= 0)
            j--;
        
        for (int k = i-1; k > j; k--)
            emp[k+1] = emp[k];
        
        emp[j+1] = insert;
    }
}

int search_employee(Employee emp[], int size){
    int id;
    cout << "Enter the id of the employee: ";
    cin >> id;
    for(int i = 0; i < size; i++){
        if(emp[i].getId() == id){
            return i;
        }
    }
    return -1;
}

void listEmployees (Employee emp[], int size) {
    for(int i = 0; i < size; i++) {
        cout << "Id: " << emp[i].getId() << ",   ";
        cout << "Name: " << emp[i].getName() << ",   ";
        cout << "Salary: " << emp[i].getSalary() << endl;
    }
}

int main (){
    Employee emp1 = Employee(101, 2000.5, "Raman");
    Employee emp2 = Employee(103, 1800.5, "Saurav");
    Employee emp3 = Employee(106, 4500.5, "Vijay");
    Employee emp4 = Employee(104, 6000.5, "Aman");
    Employee emp5 = Employee(108, 20000.5, "Patra");
    Employee emp6 = Employee(109, 200.5, "Akash");

    Employee employees[] = {emp1, emp2, emp3, emp4, emp5, emp6};

    cout << "Employee Before Sorting according their salary: \n";
    listEmployees(employees, 6);

    cout << "\n\nEmployee After Sorting according their salary: \n";
    sort_employees_by_salary(employees, 6);
    listEmployees(employees, 6);

    cout << "\n\nSearching Employee: \n";
    int index = search_employee(employees, 6);
    cout << "Employee at index: " << index;

    return 0;
}