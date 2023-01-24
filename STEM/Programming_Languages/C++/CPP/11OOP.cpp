#include <iostream>
#include <cstdlib>
#include <vector>       // for working with vectors
#include <string>       // for working with strings
#include <limits>
#include <sstream> 
#include <numeric>  // sequences
#include <ctime>    // time
#include <cmath>    // math  
#include <array> 

using namespace std; 

// Create a class 
class Student { 
    public:         // access specifier 
        int age; 
        string fName; 
        string major; 
        int grade; 

        // Constructor 
        Student(int a, string fN, string maj, int gra) {
            age = a; 
            fName = fN; 
            major = maj; 
            grade = gra; 
        }; 

        // Method definition inside class 
        void sayHello() {
            cout << fName << " : Hello!" << endl; 
        }
}; 



class Teacher {
    public: 
        int age; 
        string fName; 
        string department; 
        string position; 

        // Constructor 
        Teacher(int ag, string fN, string dep, string pos) {
            age = ag; 
            fName = fN; 
            department = dep; 
            position = pos; 
        }; 

        // Method declaration 
        void sayHello(); 
}; 

// Method definition outside class 
void Teacher::sayHello() {
    cout << "Professor : Hello." << endl; 
}

// Now a class with access specifiers 
// Public: Attributes & methods can be accessed and modified from outside the code. 
// Private: Cannot be accessed from outside the class (nor viewed) 
// Protected: Cannot be accessed from outside the class but can be accessed in inherited classes. 

// Everything is by default private if not specified

class Papers {
    public: 
        string paper1; 
        string paper2; 
        int citations; 

    private: 
        string secret1; 
        string secret2; 
        string author;
}; 

// To allow people to modify certain private attributes, you can use the setter and getter methods. 

int main(int argc, char** argv) {

    Student Muchang(21, "Muchang Bahng", "Math", 2);    // create an object of Student 
    cout << Muchang.fName << " is a " << Muchang.age << "-year old year-" << Muchang.grade << " student studying " << Muchang.major << endl; 

    Muchang.sayHello(); 

    Teacher Alec(30, "Alec Payne", "Mathematics", "Associate Professor"); 
    cout << Alec.fName << " is a " << Alec.age << "-year old " << Alec.position << " of " << Alec.department << endl; 

    Alec.sayHello(); 

    Papers Duke_Papers; 
    // Duke_Papers.paper1 = "Poincare Inequalities";        // allowed 
    // Duke_Papers.secret1 = "Secrets to World Domination"; // not allowed




    return 0; 
}