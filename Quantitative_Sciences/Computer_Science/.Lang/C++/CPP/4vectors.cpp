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

// Use vectors when you don't know the size of your array (dynamic memory)

int main(int argc, char** argv) {
    
    // Initialize vector of integers with initial size of 2
    vector<int> vNums(2); 
    vNums[0] = 1; 
    vNums[1] = 2; 
    vNums.push_back(3); // add another integer to the vector 
    cout << "Vector Size : " << vNums.size() << endl; 

    // Push words of a string into vector 
    vector<string> words; 
    stringstream ss("Some Random Words"); 
    string word; 
    while(getline(ss, word, ' ')) {
        words.push_back(word); 
    }

    return 0; 
}