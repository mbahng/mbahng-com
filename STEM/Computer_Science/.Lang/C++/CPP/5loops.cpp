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

int main(int argc, char** argv) {

    // while loop 
    int i = 1; 
    while (i <= 20) {
        if (i % 2 == 0) {
            i++; 
            continue; 
        } 
        if (i == 15) {
            break; 
        } 
        cout << i << endl; 
        i++; 
    }

    vector<string> words; 
    stringstream ss("Some Random Words"); 
    string word; 
    while(getline(ss, word, ' ')) {
        words.push_back(word); 
    }

    // for loop 
    for (int i = 0; i < words.size(); i++) {
        cout << words[i] << endl; 
    }

    for (auto x : words) {
        cout << x << endl; 
    }
    

    // Do while loop 
    srand(time(NULL)); 
    int secretNum = rand() % 11; 
    int guess = 0; 
    do {
        cout << "Guess the Number : "; 
        cin >> guess; 
        if (guess > secretNum) cout << "Too Big" << endl; 
        else if (guess < secretNum) cout << "Too Small" << endl; 
    } while (secretNum != guess); 
    cout << "You guessed it!" << endl; 

}