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

// Define function specifying the type it returns, and type of arguments
double AddNumbers(double num1 = 0.0, double num2 = 0.0) {
    return num1 + num2; 
}

// void means that it doesn't return anything 
void AssignName(); 

// We can overload functions 
int AddNumbers(int num1, int num2) { 
    return num1 + num2; 
}


int main(int argc, char** argv) {

    double x = 4.56; 
    double y = 7.4123; 
    cout << AddNumbers(x, y) << endl; 
    cout << AddNumbers(3, 7) << endl; 

    return 0; 
}

void AssignName() {
    // Assigns name "Derek" to variable name, but remember this is local! 
    string name = "Derek"; 
}