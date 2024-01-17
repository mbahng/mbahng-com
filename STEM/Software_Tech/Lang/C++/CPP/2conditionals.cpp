#include <iostream>
#include <cstdlib>
#include <vector>       // for working with vectors
#include <string>       // for working with strings
#include <limits>
#include <sstream> 
#include <numeric>  // sequences
#include <ctime>    // time
#include <cmath>    // math  

using namespace std; 

int main(int argc, char** argv) {

    // Conditional Operators : > < >= <= == != 
    // Logical Operators : && || ! 


    // If Statement 
    string sAge; 
    cout << "Enter Your Age : "; 
    cin >> sAge; 
    int nAge = stoi(sAge); 

    if ((nAge >= 1) && (nAge <= 18)) {
        cout << "Important Birthday" << endl; 
    } else if (nAge == 21 || nAge == 50 || nAge >= 65) {
        cout << "Important Birthday" << endl; 
    } else {
        cout << "Not Important Birthday" << endl; 
    }

    // Ternary Operators 
    int age43 = 43; 
    bool canIVote = (age43 >= 18) ? true : false; 

    return 0; 
}