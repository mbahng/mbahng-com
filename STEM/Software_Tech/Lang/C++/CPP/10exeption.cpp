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

// & : the address of ... 
// * : means declaring a pointers

int main(int argc, char** argv) {

    double n = 10, d = 0; 
    try {
        if (d == 0) {
            throw "Division by Zero Error"; 
        } else {
            cout << n / d << endl; 
        }
    } 

    catch(const char* exp) {
        cout << "Error : " << exp << endl; 
    }

    return 0; 
}