#include <iostream>
#include <cstdlib>
#include <vector>       // for working with vectors
#include <string>       // for working with strings
#include <limits>
#include <sstream> 
#include <numeric>  // sequences
#include <ctime>    // time
#include <cmath>    // math 
#include <typeinfo>    // for type 

using namespace std;

// variables declared outside functions are global 
int imGlobal = 0;   

// the type of the variable determines how much memory is set aside for it 
short int smallNum = 10; 
int medNum = 123532; 
long int longNum = 2e10; 

float smallDec = 1.3; 
double medDec = 12.45827; 
long double longDec = 1234.32523154; 

// variables that cannot change are constants, conventionally written all in uppercase
const double PI = 3.141; 

// Automatically assigns the type 
auto whatAmI = true; 

bool married = true; 
char myGrade = 'A'; 

int main(int argc, char** argv)
{ 
    // Print statement 
    std::cout << "Hello World" << endl; 

    cout << "short int Byte : " << sizeof(short int) << endl; 
    cout << "int Byte : " << sizeof(int) << endl; 
    cout << "long int Byte : " << sizeof(long int) << endl; 

    cout << "float Byte : " << sizeof(float) << endl; 
    cout << "double Byte : " << sizeof(double) << endl; 
    cout << "long double Byte : " << sizeof(long double) << endl; 

    // Strings can be initialized or not 
    string q1 = "Enter a number : "; 
    string num1, num2; 
    cout << q1;             // print out 
    cin >> num1;     // take in as input and store as num1 
    cout << "Enter Another Number : "; 
    cin >> num2; 

    // Converting String to integer: stoi(int) 
    // Converting String to float  : stof(int) 
    int nNum1 = stoi(num1); 
    int nNum2 = stoi(num2); 
    printf("%d + %d = %d\n", nNum1, nNum2, nNum1 + nNum2); 

    // Printing booleans as True or False, as opposed to 1 and 0
    cout << married << endl; // 1 or 0 
    cout.setf(ios::boolalpha); 
    cout << married << endl; // true or false 

    // Get type of variable 
    cout << typeid(married).name() << endl; 
    return 0; 
}