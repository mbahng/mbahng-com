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
    
    // Assign value 4 to variable X
    int X = 4; 

    // int* means that the variable points to an integer 
    // & : the address of ... 
    // Conventional to use pX to denote it's a pointer to X 
    int* pX = &X; 

    cout << "Address : " << pX << endl; 
    cout << "Value : " << *pX << endl; 
    
    // integer named y is set to the thing pointed to by pX
    // This allows us to pass around X by reference rather than value 
    int y = *pX; 

    return 0; 
}