#include <iostream>
#include <algorithm>
#include <string>

using namespace std;

// Enumeration for Alphabet (A-Z mapped to 0-25)
enum class Alphabet {
    A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z
};

// Function to convert Numbers to Alphabets.
char toAlpha(Alphabet ele) {
    return 'A' + static_cast<int>(ele);
}

// Function to convert Alphabet to Numbers
Alphabet toNumber(char c) {
    if (c >= 'A' && c <= 'Z')
        return static_cast<Alphabet>(c - 'A');

    // Handle the other character rather than Alphabets.
    throw invalid_argument("Character must be between 'A' and 'Z'");
}

// Function to remove space.
string removeSpaces(string &str) {
    str.erase(remove(str.begin(), str.end(), ' '), str.end());
    return str;
}

// Function to convert plaintext to ciphertext using a Vigener cipher.
string plainToCipher(string &plainText, string &key) {
    plainText = removeSpaces(plainText);    // remove space.
    string cipherText = "";                 // Cipher text.
    int plainTextSize = plainText.length(); // Determine the size of plain text.
    int keySize = key.length();             // Determine the size of key.

    if (keySize == 0)
        throw invalid_argument("Key cannot be empty");

    for (int i = 0; i < plainTextSize; i++) {
        char plainChar = toupper(plainText[i]);   // Convert plaintext to uppercase.
        char keyChar = toupper(key[i % keySize]); // Convert key to uppercase.

        // Append encrypt character.
        int addAlpha = (static_cast<int>(toNumber(plainChar)) + static_cast<int>(toNumber(keyChar))) % 26;
        cipherText += toAlpha(static_cast<Alphabet>(addAlpha));
    }

    return cipherText;
}

int main() {
    string plainText, key;
    cout << "Enter your Plain Text here: ";
    getline(cin, plainText);

    cout << "Enter your Key here: ";
    getline(cin, key);

    cout << "Cipher text of Plain text: " << plainToCipher(plainText, key);
    return 0;
}
