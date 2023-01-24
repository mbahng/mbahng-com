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

// Arrays are sequences that have static memory

using namespace std; 

int main(int argc, char** argv) {

    // Initialize an array of integers with memory for 10 values (can't be changed)
    int arrnNums[10] = {1};     // Initialize with just a 1 in it 

    // If not specified, the size is automatically what you put it as 
    int arrnNums2[] = {1, 2, 3}; 
    int arrnNums3[5] = {8, 9};

    // Indexing 
    cout << "1st Value : " << arrnNums3[0] << endl; 
    arrnNums3[0] = 7; 
    cout << "1st Value : " << arrnNums3[0] << endl; 

    // Multidimensional arrays
    int arrnNums4[2][2][2] = {{{1, 2}, {3, 4}}, {{5, 6}, {7, 8}}}; 
    cout << arrnNums4[0][0][0] << endl; 

    return 0; 
}