#include <iostream>
#include <string>
#include <cctype>
#include <algorithm>

using namespace std;

bool containsSubstring(const string& str, const string& substr) {
    string str_lower = str;
    string substr_lower = substr;
    transform(str_lower.begin(), str_lower.end(), str_lower.begin(), ::tolower);
    transform(substr_lower.begin(), substr_lower.end(), substr_lower.begin(), ::tolower);

    return str_lower.find(substr_lower) != string::npos;
}

class PersonInformation {
protected:
    string name;
    string emailId;
    string roomNumber;
    string positionName;
    string telephoneNumber;

public:
    PersonInformation(string name, string telephoneNumber, string emailId, string roomNumber, string positionName) {
        this->name = name;
        this->emailId = emailId;
        this->roomNumber = roomNumber;
        this->positionName = positionName;
        this->telephoneNumber = telephoneNumber;
    }

    void getInformation(string department) {
        cout << this->name << "  ( " << this->positionName << " )" << endl;
        cout << "-----------------------------------------------------------" << endl;
        cout << "   Department          : " << department << endl;
        cout << "   Email Id            : " << this->emailId << endl;
        cout << "   Telephone Number    : " << this->telephoneNumber << endl;
        cout << "   Room Number         : " << this->roomNumber << endl;
    }

    string getName() {
        return this->name;
    }
};

class AdministrativeDepartment : public PersonInformation {
protected:
    string departmentName;

public:
    AdministrativeDepartment(string name, string telephoneNumber, string emailId, string roomNumber, string positionName)
        : PersonInformation(name, telephoneNumber, emailId, roomNumber, positionName) {}

    void printInformation() {
        cout << endl;
        getInformation(this->departmentName);
        cout << endl;
    }

    void setDepartmentName(const string& name) {
        departmentName = name;
    }

    string getDepartmentName() const {
        return departmentName;
    }
};

class InnovationResearchAndDevelopment : public AdministrativeDepartment {
public:
    InnovationResearchAndDevelopment(string name, string telephoneNumber, string emailId, string roomNumber, string positionName)
        : AdministrativeDepartment(name, telephoneNumber, emailId, roomNumber, positionName) {
        this->departmentName = "Innovation Research & Development";
    }
};

class Academics : public AdministrativeDepartment {
public:
    Academics(string name, string telephoneNumber, string emailId, string roomNumber, string positionName)
        : AdministrativeDepartment(name, telephoneNumber, emailId, roomNumber, positionName) {
        this->departmentName = "Academics";
    }
};

class StudentAffairs : public AdministrativeDepartment {
public:
    StudentAffairs(string name, string telephoneNumber, string emailId, string roomNumber, string positionName)
        : AdministrativeDepartment(name, telephoneNumber, emailId, roomNumber, positionName) {
        this->departmentName = "Student Affairs";
    }
};

class StoreAndPurchase : public AdministrativeDepartment {
public:
    StoreAndPurchase(string name, string telephoneNumber, string emailId, string roomNumber, string positionName)
        : AdministrativeDepartment(name, telephoneNumber, emailId, roomNumber, positionName) {
        this->departmentName = "Store & Purchase";
    }
};

class Library : public AdministrativeDepartment {
public:
    Library(string name, string telephoneNumber, string emailId, string roomNumber, string positionName)
        : AdministrativeDepartment(name, telephoneNumber, emailId, roomNumber, positionName) {
        this->departmentName = "Library";
    }
};

class Registrar {
    AdministrativeDepartment* adminDepartments[100];
    int departmentCount = 0;

public:
    void addDepartment(AdministrativeDepartment* dept) {
        if (departmentCount < 100) {
            adminDepartments[departmentCount++] = dept;
        }
    }

    void fetchInformation(string name) {
        cout << name << endl;
        for (int i = 0; i < departmentCount; ++i) {
            if (containsSubstring(adminDepartments[i]->getName(), name)) {
                cout << adminDepartments[i]->getName() << endl;
                adminDepartments[i]
                    ->printInformation();
                return;
            }
        }
        cout << "Person does not exist in any Administrative Departments!" << endl;
    }
};

void assignDepartments(Registrar& registrar) {
    // Assign Departments
    // IDR Departments
    registrar.addDepartment(new InnovationResearchAndDevelopment("Vivek Ashok Bohara", "+91-11-26907446", "dird@iiitd.ac.in", "None", "Dean"));
    registrar.addDepartment(new InnovationResearchAndDevelopment("Debarka Sengupta", "+91-11-26907454", "adird@iiitd.ac.in", "None", "Associate Dean"));
    registrar.addDepartment(new InnovationResearchAndDevelopment("Mohit Kumar", "011 26907 505", "mohit@iiitd.ac.in", "A-311 (Academic Block)", "Assistant Administrative Officer"));
    registrar.addDepartment(new InnovationResearchAndDevelopment("Imran Khan", "011 26907 594", "imran@iiitd.ac.in", " A-307 (Academic Block)", "Junior Administrative Officer"));
    registrar.addDepartment(new InnovationResearchAndDevelopment("Kapil Dev Garg", "011 26907 119", "kapildev@iiitd.ac.in", " A-306 (Academic Block)", "Administrative Officer"));

    // Academics Departments
    registrar.addDepartment(new Academics("Sumit J Darak", "+91-11-26907427", "doaa@iiitd.ac.in", "None", "Dean"));
    registrar.addDepartment(new Academics("Aakash Gupta", "011 26907 135", "aakash@iiitd.ac.in", "B-207 (Academic Block)", "Junior Administrative Officer"));
    registrar.addDepartment(new Academics("Akanksha", "011 26907 140", "akanksha@iiitd.ac.in", "B-207(Academic Block)", "Junior Administrative Officer"));
    registrar.addDepartment(new Academics("Anshu Dureja", "011 26907 507", "anshu@iiitd.ac.in", "B-208 (Academic Block)", "Deputy Administrative Officer"));
    registrar.addDepartment(new Academics("Ashish Aggarwal", "011 26907 136", "ashisha@iiitd.ac.in", "B-207 (Academic Block)", "Junior Administrative Officer"));
    registrar.addDepartment(new Academics("Ashutosh Brahma", "011 26907 416", "ashutosh@iiitd.ac.in", "B-202 (Academic Block)", "Administrative Officer"));
    registrar.addDepartment(new Academics("Nisha Narwal", "011 26907 483", "nisha@iiitd.ac.in", "B-207 (Academic Block)", "Assistant Administrative Officer"));
    registrar.addDepartment(new Academics("Prachi Mukherjee", "011 26907 545", "prachi@iiitd.ac.in", "B-207 (Academic Block)", "Assistant Administrative Officer"));
    registrar.addDepartment(new Academics("Raju Biswas", "011 26907 137", "raju@iiitd.ac.in", "B-208 (Academic Block)", "Junior Administrative Officer"));
    registrar.addDepartment(new Academics("Sanjana Soni", "011 26907 129", "sanjanas@iiitd.ac.in", "B-207(Academic Block)", "Junior Administrative Officer"));
    registrar.addDepartment(new Academics("Sudhanshu Tamta", "011 26907 117", "sudhanshut@iiitd.ac.in", "B-207 (Academic Block)", "Junior Administrative Officer"));

    // Student Affairs Departments
    registrar.addDepartment(new StudentAffairs("Shobha Sundar Ram", "+91-11-26907460", "dosa@iiitd.ac.in", "None", "Dean"));
    registrar.addDepartment(new StudentAffairs("Dr. Ravi Bhasin", "011 26907 504", "ravi@iiitd.ac.in", "A-207-1 (Academic Block)", "Administrative Officer"));
    registrar.addDepartment(new StudentAffairs("Jagadanand Dwivedi", "011 26907 421", "jagadanand@iiitd.ac.in", "A-207-1 (Academic Block)", "Junior Administrative Officer"));
    registrar.addDepartment(new StudentAffairs("Sonal Garg", "011 26907 553", "sonal@iiitd.ac.in", "A-207-1 (Academic Block)", "Junior Administrative Officer"));

    // Store and Purchase Departments
    registrar.addDepartment(new StoreAndPurchase("Sangam Kumar YadavAmit", "011 26907 400", "sangam@iiitd.ac.in", "A-106, Academic Block", "Junior Administrative Officer"));
    registrar.addDepartment(new StoreAndPurchase("Nidhi Yadav", "011 26907 597", "nidhi@iiitd.ac.in", "A-108 (Academic Block)", "Assistant Administrative Officer"));
    registrar.addDepartment(new StoreAndPurchase("Ajay Kumar", "011 26907 561", "ajay@iiitd.ac.in", "A-103(2) (Academic Block)", "Administrative Officer"));

    // Library
    registrar.addDepartment(new Library("Rajendra Singh", "011 26907 510", "rajendra@iiitd.ac.in", "Library Block", "Library Officer"));
    registrar.addDepartment(new Library("Amit Kumar", "011 26907 511", "amit@iiitd.ac.in", "Library Block", "Assistant Library Officer"));
}

bool checkAlpha(string name) {
    for(char c : name) {
        if(c != ' ' && !isalpha(c)) {
            return false;
        }
    }
    return true;
}

int main() {
    Registrar registrar;
    assignDepartments(registrar);
    
    string name;
    cout << "Enter the name of the person to fetch their information: ";
    getline(cin, name);

    if (!checkAlpha(name))
        cout << "Invalid Name..." << endl;
    else
        registrar.fetchInformation(name);

    return 0;
}
