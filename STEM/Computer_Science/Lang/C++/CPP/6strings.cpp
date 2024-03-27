#include <iostream>
#include <cstdlib>
#include <vector>       // for working with vectors
#include <string>       // for working with strings
#include <sstream> 

using namespace std; 

int main(int argc, char** argv) {
    string str1 = "I'm a string"; 

    // First and last characters 
    cout << "1st : " << str1[0] << endl; 
    cout << "Last : " << str1.back() << endl; 

    // Length of string 
    cout << "Length : " << str1.length() << endl; 

    // Copy strings 
    string str2 = str1; 
    string str3(str2, 4); // str3 = str2[4:]
    cout << str3 << endl; 

    // Add to strings 
    string str4 = str1 + " and you're not"; 
    str4.append("!"); 
    cout << "Old String " << str4 << endl; 

    // Delete from strings 
    str4.erase(12, str4.length() - 1); // delete from index 12 to end
    cout << "New String " << str4 << endl; 

    // find starting index of substring 
    cout << str4.find("string") << endl; 

    // substr(x, y) function returns substring starting at index x with length y
    cout << str4.substr(6, 6) << endl; 

    // Convert int to string 
    string strNum = to_string(3); 
    cout << typeid(strNum).name() << endl; 

    // String interpolation with printf
    // %c char, %d int, %5d 5 spaces, %.3f float with 3 dec places, %s string)
    printf("%c %d %5d %.3f %s\n", 'A', 10, 6,5.33425, "hello"); 

    // Checking types 
    char letterZ = 'z'; 
    char num5 = '5'; 
    char aSpace = ' '; 
    cout << isalnum(letterZ) << endl; // check if letter OR number 
    cout << isalpha(letterZ) << endl; // check if letter 
    cout << isdigit(num5) << endl;    // check if number 
    cout << isspace(aSpace) << endl;  // check if a space 

    return 0; 
}