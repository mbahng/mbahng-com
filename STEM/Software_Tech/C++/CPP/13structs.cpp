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

// Structs more for data structures than classes 
// By default everything is public 

struct Shape {
    double length; 
    double width; 
    
    // Constructor 
    Shape(double l = 1, double w = 1) {
        length = l; 
        width = w; 
    }

    double Area() {
        return length * width; 
    }
    
private: 
    int id; 
}; 

// Child structs 
struct Circle : Shape {
    // Override constructor 
    Circle(double width) {
        this -> width = width; 
    } 

    double Area() {
        return 3.14159 * pow((width/2), 2); 
    }
}; 

int main(int argc, char** argv) {

    return 0; 
}