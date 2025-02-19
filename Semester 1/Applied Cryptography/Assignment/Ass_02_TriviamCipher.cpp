#include <iostream>
#include <iomanip>
#include <bitset>
#include <algorithm>
#include <sstream>
#include <string>
#include <vector>

using namespace std;

// Define the sizes in bits for the key, initialization vector (IV), and keystream
#define KEY_SIZE 80
#define IV_SIZE 80
#define KEY_STREAM_SIZE 512 // Fixed size of the generated keystream

// Class implementing the Trivium Cipher
class TriviumCipher
{
    // Three internal bitstreams of varying sizes used in the Trivium algorithm
    bitset<93> streamOne;    // First stream of 93 bits
    bitset<84> streamTwo;    // Second stream of 84 bits
    bitset<111> streamThree; // Third stream of 111 bits

public:
    // Constructor that initializes the Trivium cipher state using the given IV and KEY
    TriviumCipher(const bitset<IV_SIZE> &IV, const bitset<KEY_SIZE> &KEY)
    {
        // Initialize the internal streams using the key and IV
        setStream(KEY, streamOne, 80, 93);
        setStream(IV, streamTwo, 80, 84);

        // Set the last three bits of the third stream to 1 as part of the initialization
        streamThree.set(110, 1);
        streamThree.set(109, 1);
        streamThree.set(108, 1);
    }

    // Function to reverse each byte (8 bits) of the bitset
    void revKeystreamBits(bitset<KEY_STREAM_SIZE> &keyStream)
    {
        for (size_t i = 0; i < KEY_STREAM_SIZE; i += 8)
        {
            // Extract 8 bits
            bitset<8> byte;
            for (size_t j = 0; j < 8; j++)
                byte[j] = keyStream[i + j];

            // Reverse the 8 bits
            for (size_t j = 0; j < 8; j++)
                keyStream[i + j] = byte[7 - j];
        }
    }

    // Function to copy bits from a source bitset into a destination bitset and pad the rest with zeros
    template <size_t sd1, size_t sd2>
    void setStream(const bitset<sd1> &source, bitset<sd2> &destination, int keySize, int streamSize)
    {
        // Copy keySize bits from the source to the destination bitset
        for (int i = 0; i < keySize; i++)
        {
            destination[i] = source[i];
        }
        // Pad the remaining bits with zeros up to the streamSize
        for (int i = keySize; i < streamSize; i++)
        {
            destination[i] = 0;
        }
    }

    // Function to generate the keystream of fixed length (KEY_STREAM_SIZE)
    bitset<KEY_STREAM_SIZE> genKeyStream()
    {
        bitset<KEY_STREAM_SIZE> keyStream; // Bitset to store the generated keystream

        // Warm-up phase to initialize the internal state by running the updator function 197 times
        for (int i = 0; i < 1152; i++)
            updator();

        // Generate the keystream by continuously updating the state and capturing output bits
        for (int i = 0; i < KEY_STREAM_SIZE; i++)
            keyStream[KEY_STREAM_SIZE - i - 1] = updator();

        revKeystreamBits(keyStream);
        return keyStream; // Return the generated keystream
    }

private:
    // Function to update the internal state of the Trivium cipher and produce a single output bit
    bool updator()
    {
        // Calculate feedback and output bits based on XOR and AND operations on the internal streams
        bool t1 = streamOne[65] ^ streamOne[92];
        bool t2 = streamTwo[68] ^ streamTwo[83];
        bool t3 = streamThree[65] ^ streamThree[110];
        bool kbit = t1 ^ t2 ^ t3; // Final output bit from the three streams

        // Update the feedback bits for each stream based on non-linear functions
        bool sb1 = t1 ^ (streamOne[91] & streamOne[90]) ^ streamTwo[77];
        bool sb2 = t2 ^ (streamTwo[82] & streamTwo[81]) ^ streamThree[86];
        bool sb3 = t3 ^ (streamThree[109] & streamThree[108]) ^ streamOne[68];

        // Shift each stream left by one bit, effectively pushing all bits one position to the left
        streamOne <<= 1;
        streamTwo <<= 1;
        streamThree <<= 1;

        // Insert the calculated feedback bits into the streams
        streamOne[0] = sb3;
        streamTwo[0] = sb1;
        streamThree[0] = sb2;

        return kbit; // Return the generated output bit
    }
};

// Function to convert a hexadecimal string to a binary string representation
string hexToBinary(const string &hex)
{
    string binaryString = ""; // String to store the binary representation
    // Loop through each hexadecimal character and convert to its binary equivalent
    for (char c : hex)
    {
        switch (toupper(c))
        { // Convert character to uppercase to handle both cases
        case '0':
            binaryString += "0000";
            break;
        case '1':
            binaryString += "0001";
            break;
        case '2':
            binaryString += "0010";
            break;
        case '3':
            binaryString += "0011";
            break;
        case '4':
            binaryString += "0100";
            break;
        case '5':
            binaryString += "0101";
            break;
        case '6':
            binaryString += "0110";
            break;
        case '7':
            binaryString += "0111";
            break;
        case '8':
            binaryString += "1000";
            break;
        case '9':
            binaryString += "1001";
            break;
        case 'A':
            binaryString += "1010";
            break;
        case 'B':
            binaryString += "1011";
            break;
        case 'C':
            binaryString += "1100";
            break;
        case 'D':
            binaryString += "1101";
            break;
        case 'E':
            binaryString += "1110";
            break;
        case 'F':
            binaryString += "1111";
            break;
        }
    }
    return binaryString; // Return the full binary representation
}

// Function to convert a bitset of the keystream to a hexadecimal string
string bitsetToHex(const bitset<KEY_STREAM_SIZE> &bits)
{
    stringstream ss;
    ss << hex << uppercase << setfill('0'); // Set formatting options for hexadecimal output
    // Loop through bits in groups of 4 to convert to hexadecimal
    for (size_t i = bits.size(); i > 0; i -= 4)
    {
        // Extract four bits at a time and convert to a single hex digit
        int val = (bits[i - 1] << 3) | (bits[i - 2] << 2) | (bits[i - 3] << 1) | bits[i - 4];
        ss << val;
    }
    return ss.str(); // Return the hexadecimal string representation
}

// Function to convert a string to a bitset of the same size as the keystream
bitset<KEY_STREAM_SIZE> stringToBitset(const string &str)
{
    string binaryString = ""; // Binary representation of the string
    // Loop through each character of the string and convert to binary
    for (char c : str)
    {
        bitset<8> charBits(c);                // Convert character to a bitset of 8 bits
        binaryString += charBits.to_string(); // Append the binary string
    }
    // Return a bitset initialized with the binary string, truncated or padded as necessary
    return bitset<KEY_STREAM_SIZE>(binaryString);
}

// Function to convert a bitset to a string representation
string bitsetToString(const bitset<KEY_STREAM_SIZE> &bits)
{
    stringstream ss;
    // Convert the bitset back to a string by grouping bits into bytes
    for (size_t i = 0; i < bits.size(); i += 8)
    {
        bitset<8> charBits;
        // Extract 8 bits at a time and form a character
        for (size_t j = 0; j < 8; j++)
        {
            charBits[j] = bits[i + j];
        }
        ss << char(charBits.to_ulong()); // Convert bits to a character and append to string
    }
    return ss.str(); // Return the reconstructed string
}

// Function to encrypt a message by XORing it with the keystream
string encryptMessage(const string &message, const bitset<KEY_STREAM_SIZE> &keyStream)
{
    bitset<KEY_STREAM_SIZE> messageBits = stringToBitset(message);   // Convert the message to bits
    bitset<KEY_STREAM_SIZE> encryptedBits = messageBits ^ keyStream; // XOR message bits with keystream bits
    return bitsetToString(encryptedBits);                            // Convert the encrypted bits back to a string and return
}
string reverseInPairs(const string &input)
{
    vector<string> pairs;

    // Split the string into pairs of two characters
    for (size_t i = 0; i < input.length(); i += 2)
    {
        pairs.push_back(input.substr(i, 2));
    }

    // Reverse the order of pairs
    reverse(pairs.begin(), pairs.end());

    // Combine the reversed pairs into a single string
    string result;
    for (const auto &pair : pairs)
    {
        result += pair;
    }

    return result;
}

int main()
{
    string iv, key, message;

    // Prompt the user for the IV and key values
    cout << "Please, Enter your IV and KEY: " << endl;
    cout << "Enter IV: ";
    cin >> iv;
    cout << "Enter KEY: ";
    cin >> key;

    // Ensure the input values are of correct length, i.e., 20 hexadecimal digits for IV and KEY
    if (iv.length() != IV_SIZE / 4 || key.length() != KEY_SIZE / 4)
    {
        cout << "IV and KEY must be exactly " << IV_SIZE / 4 << " and " << KEY_SIZE / 4
             << " hexadecimal digits respectively." << endl;
        return 1; // Exit with an error if the lengths are incorrect
    }

    // Convert the hexadecimal IV and KEY values to binary strings
    iv = reverseInPairs(iv);
    key = reverseInPairs(key);
    // reverse(iv.begin(), iv.end());
    // reverse(key.begin(), key.end());
    string ivVal = hexToBinary(iv);
    string keyVal = hexToBinary(key);

    // Initialize the IV and KEY as bitsets
    bitset<IV_SIZE> IV(ivVal);
    bitset<KEY_SIZE> KEY(keyVal);

    // Create an instance of the TriviumCipher class with the IV and KEY
    TriviumCipher trivium(IV, KEY);

    // Generate the keystream
    bitset<KEY_STREAM_SIZE> keyStream = trivium.genKeyStream();
    cout << "Generated Keystream: " << bitsetToHex(keyStream) << endl;

    // Prompt the user to enter a message for encryption
    cout << "Enter message to encrypt: ";
    cin.ignore(); // Clear the input buffer before reading the message
    getline(cin, message);

    // Encrypt the message using the generated keystream
    string encryptedMessage = encryptMessage(message, keyStream);
    cout << "Encrypted Message: " << encryptedMessage << endl;

    return 0; // End the program
}

// Test Cases:
// Key = 00000000000000000000
// IV = 00000000000000000000
// keystream = FBE0BF265859051B517A2E4E239FC97F563203161907CF2DE7A8790FA1B2E9CDF75292030268B7382B4C1A759AA2599A285549986E74805903801A4CB5A5D4F2
// Key = 80000000000000000000
// IV = 00000000000000000000
// keystream = 38EB86FF730D7A9CAF8DF13A4420540DBB7B651464C87501552041C249F29A64D2FBF515610921EBE06C8F92CECF7F8098FF20CCCC6A62B97BE8EF7454FC80F9
