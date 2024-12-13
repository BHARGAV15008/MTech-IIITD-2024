#include <iostream>
#include <string>
#include <cctype>
#include <algorithm>
#define MAX_DEPARTMENTS 100
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
    PersonInformation() {}

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

class AcademicDepartments : public PersonInformation {
protected:
    string departmentName;

public:
    AcademicDepartments(string name, string telephoneNumber, string emailId, string roomNumber, string positionName)
        : PersonInformation(name, telephoneNumber, emailId, roomNumber, positionName) {}

    void printInformation() {
        cout << endl;
        this->getInformation(this->departmentName);
        cout << endl;
    }

    void setDepartmentName(const string& name) {
        departmentName = name;
    }
};

class ComputationBiology : public AcademicDepartments {
public:
    ComputationBiology(string name, string telephoneNumber, string emailId, string roomNumber, string positionName)
        : AcademicDepartments(name, telephoneNumber, emailId, roomNumber, positionName) {
        setDepartmentName("Computational Biology");
    }
};

class ComputerScience : public AcademicDepartments {
public:
    ComputerScience(string name, string telephoneNumber, string emailId, string roomNumber, string positionName)
        : AcademicDepartments(name, telephoneNumber, emailId, roomNumber, positionName) {
        setDepartmentName("Computer Science & Engineering");
    }
};

class ElectronicsCommunications : public AcademicDepartments {
public:
    ElectronicsCommunications(string name, string telephoneNumber, string emailId, string roomNumber, string positionName)
        : AcademicDepartments(name, telephoneNumber, emailId, roomNumber, positionName) {
        setDepartmentName("Electronics & Communications Engineering");
    }
};

class SocialSciencesAndHumanities : public AcademicDepartments {
public:
    SocialSciencesAndHumanities(string name, string telephoneNumber, string emailId, string roomNumber, string positionName)
        : AcademicDepartments(name, telephoneNumber, emailId, roomNumber, positionName) {
        setDepartmentName("Social Sciences & Humanities");
    }
};

class HumanCenteredDesign : public AcademicDepartments {
public:
    HumanCenteredDesign(string name, string telephoneNumber, string emailId, string roomNumber, string positionName)
        : AcademicDepartments(name, telephoneNumber, emailId, roomNumber, positionName) {
        setDepartmentName("Human Centered Design");
    }
};

class Academics {
    AcademicDepartments* academics[MAX_DEPARTMENTS];
    int count;

public:
    Academics() : count(0) {}

    void addDepartment(AcademicDepartments* dept) {
        if (count < MAX_DEPARTMENTS) {
            academics[count++] = dept;
        } else {
            cout << "Maximum number of departments reached!" << endl;
        }
    }

    void fetchInformation(string name) {
        for (int i = 0; i < count; i++) {
            if (containsSubstring(academics[i]->getName(), name)) {
                academics[i]->printInformation();
                return;
            }
        }
        cout << "Person not Exist in Any Administrative Departments!" << endl;
    }
};

void assignDepartments(Academics &academics) {
    // Add faculty members to the Departments
    academics.addDepartment(new ComputationBiology("Arjun Ray", "011-26907438", "arjun@iiitd.ac.in", "A-310 (R&D Block)", "Assistant Professor"));
    academics.addDepartment(new ComputationBiology("Jaspreet Kaur Dhanjal", "011-26907522", "jaspreet@iiitd.ac.in", "A-307 (R&D Block)", "Assistant Professor"));
    academics.addDepartment(new ComputationBiology("Sriram K", "011-26907436", "sriramk@iiitd.ac.in", "A-308 (R&D Block)", "Associate Professor"));
    academics.addDepartment(new ComputationBiology("Gaurav Ahuja", "011-26907475", "gaurav.ahuja@iiitd.ac.in", "A-303 (R&D Block)", "Associate Professor"));
    academics.addDepartment(new ComputationBiology("Tavpritesh Sethi", "011 26907 533", "tavpriteshsethi@iiitd.ac.in", "A-309 (R&D Block)", "Associate Professor"));

    academics.addDepartment(new ComputerScience("Arani Bhattacharya", "011-26907434", "arani@iiitd.ac.in", "B-510 (R&D Block)", "Assistant Professor"));
    academics.addDepartment(new ComputerScience("Bapi Chatterjee", "011-26907371", "bapi@iiitd.ac.in", "B-402 (R&D Block)", "Assistant Professor"));
    academics.addDepartment(new ComputerScience("Debajyoti Bera", "011-26907442", "dbera@iiitd.ac.in", "B-508 (R&D Block)", "Associate Head & Associate Professor"));
    academics.addDepartment(new ComputerScience("Vinayak Abrol", "011-26907543", "abrol@iiitd.ac.in", "B-409 (R&D Block)", "Assistant Professor"));
    academics.addDepartment(new ComputerScience("Syamantak Das", "011-26907529", "syamantak@iiitd.ac.in", "B-505, (R&D Block)", "Assistant Professor"));

    academics.addDepartment(new ElectronicsCommunications("Abhijit Mitra", "+91 011-26907450", "abhijit@iiitd.ac.in", "A-605 (R&D Block)", "Assistant Professor"));
    academics.addDepartment(new ElectronicsCommunications("Anubha Gupta", "011-26907428", "anubha@iiitd.ac.in", "B-609 (R&D Block)", "Professor"));
    academics.addDepartment(new ElectronicsCommunications("Anuj Grover", "011-26907494", "anuj@iiitd.ac.in", "A-610 (R&D Block)", "Associate Professor"));
    academics.addDepartment(new ElectronicsCommunications("Chanekar Prasad Vilas", "011-26907374", "prasad@iiitd.ac.in", "B-610 (R&D Block)", "Assistant Professor"));
    academics.addDepartment(new ElectronicsCommunications("Manuj Mukherjee", "011-26907376", "manuj@iiitd.ac.in", "A-608 (R&D Block)", "Assistant Professor"));

    academics.addDepartment(new SocialSciencesAndHumanities("Manohar Kumar", "011 26907 557", "manohar.kumar@iiitd.ac.in", "B-207 (R & D Block)", "Head, Assistant Professor"));
    academics.addDepartment(new SocialSciencesAndHumanities("Deepak Prince", "011 26907 595", "deepak@iiitd.ac.in", "A-210 (R & D Block)", "Assistant Professor"));
    academics.addDepartment(new SocialSciencesAndHumanities("Mrinmoy Chakrabarty", "011 26907 363", "mrinmoy@iiitd.ac.in", "A-202 (R & D Block)", "Assistant Professor"));
    academics.addDepartment(new SocialSciencesAndHumanities("Soibam Haripriya", "011 26907 360", "soibam@iiitd.ac.in", "A-204 (R & D Block)", "Assistant Professor"));
    academics.addDepartment(new SocialSciencesAndHumanities("Kiriti Kanjilal", "011 26907 558", "kanjilal@iiitd.ac.in", "B-208 (R & D Block)", "Assistant Professor"));

    academics.addDepartment(new HumanCenteredDesign("Anmol Srivastava", "011-26907467", "anmol@iiitd.ac.in", "A-404 (R&D Block)", "Assistant Professor"));
    academics.addDepartment(new HumanCenteredDesign("Jainendra Shukla", "011-26907523", "jainendra@iiitd.ac.in", "A-410 (R&D Block)", "Assistant Professor"));
    academics.addDepartment(new HumanCenteredDesign("Rajiv Ratn Shah", "011-26907495", "rajivratn@iiitd.ac.in", "A-409 (R&D Block)", "Associate Professor"));
    academics.addDepartment(new HumanCenteredDesign("Kalpana Shankhwar", "011-26907496", "kalpana@iiitd.ac.in", "A-403 (R&D Block)", "Assistant Professor"));
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
    // Generate Departments and Assign their Head
    ComputationBiology cbH("G.P.S. Raghava", "011-26907444", "raghava@iiitd.ac.in", "A-302 (R&D Block)", "Head & Professor");
    ComputerScience cseH("Sambuddho", "011-26907478", "sambuddho@iiitd.ac.in", "B-503 (R&D Block)", "Head (CSE) & Associate Professor");
    ElectronicsCommunications eceH("A V Subramanyam", "+91 011-26907437", "subramanyam@iiitd.ac.in", "B-604 (R&D Block)", "Head (ECE) & Associate Professor");
    SocialSciencesAndHumanities sshH("J. V. Meenakshi", "011 26907 535", "meena@iiitd.ac.in", "B-205 (R & D Block)", "Head, Professor");
    HumanCenteredDesign hcdH("Richa Gupta", "011-26907368", "richa.gupta@iiitd.ac.in", "A-406 (R&D Block)", "Head (HCD), Assistant Professor");

    // Assign administrative officers
    ComputationBiology cbA("Shipra Jain", "011 26907 412", "shipra@iiitd.ac.in", "A-301 (R&D Block)", "Assistant Administrative Officer");
    ComputerScience cseA("Priti Patwal", "011 26907 411", "pritip@iiitd.ac.in", "A-501 (R&D Block)", "Assistant Administrative Officer");
    ElectronicsCommunications eceA("Sanjna Khosla", "011 26907 593", "sanjna@iiitd.ac.in", "A-601 (R&D Block)", "Assistant Administrative Officer");
    SocialSciencesAndHumanities sshA("Rubina Thakur", "011 26907 497", "rubina@iiitd.ac.in", "B-201 (R&D Block)", "Junior Administrative Officer");
    HumanCenteredDesign hcdA("Binu Ann Joseph", "011 26907 588", "binu@iiitd.ac.in", "A-401 (R&D Block)", "Junior Administrative Officer");

    Academics academics;
    assignDepartments(academics);

    academics.addDepartment(&cbH);
    academics.addDepartment(&cseH);
    academics.addDepartment(&eceH);
    academics.addDepartment(&sshH);
    academics.addDepartment(&hcdH);

    academics.addDepartment(&cbA);
    academics.addDepartment(&cseA);
    academics.addDepartment(&eceA);
    academics.addDepartment(&sshA);
    academics.addDepartment(&hcdA);

    // Fetch information of the Faculty which Belonging to Departments
    string nameToSearch;
    cout << "Enter the name of the person who is present in any department : ";
    getline(cin, nameToSearch);

    if (!checkAlpha(nameToSearch))
        cout << "Invalid Name..." << endl;
    else
        academics.fetchInformation(nameToSearch);

    return 0;
}