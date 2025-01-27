# Group Member: Ritesh Gupta (MT24132)

# Initial Permutation Table
initialPermutationTable = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Expansion Table
expansionTable = [
    32, 1, 2, 3, 4, 5, 4, 5,
    6, 7, 8, 9, 8, 9, 10, 11,
    12, 13, 12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21, 20, 21,
    22, 23, 24, 25, 24, 25, 26, 27,
    28, 29, 28, 29, 30, 31, 32, 1
]

# Permutation Table
permutationTable = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

# S-Boxes
sBoxes = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8,  15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15,  3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

# Final Permutation Table
finalPermutationTable = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

# Key Permutation Table
keyPermutationTable = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

# Key Schedule Shifts
keyScheduleShifts = [
    1, 1, 2, 2,
    2, 2, 2, 2,
    1, 2, 2, 2,
    2, 2, 2, 1
]

# Key Schedule Table
keyScheduleTable = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

# Function to convert a hexadecimal string to a binary string
def hexToBinary(input):
    # Mapping of hexadecimal characters to their binary equivalents
    mappingHB = {
        '0': "0000", '1': "0001", '2': "0010", '3': "0011",
        '4': "0100", '5': "0101", '6': "0110", '7': "0111",
        '8': "1000", '9': "1001", 'A': "1010", 'B': "1011",
        'C': "1100", 'D': "1101", 'E': "1110", 'F': "1111"
    }
    
    # Initialize an empty string to store the binary representation
    toBinary = ""
    
    # Iterate over each character in the input hexadecimal string
    for i in range(len(input)):
        # Append the binary equivalent of the current character to the result string
        toBinary = toBinary + mappingHB[input[i]]
    
    # Return the binary string
    return toBinary


# Function to convert a binary string to a hexadecimal string
def binaryToHex(input):
    # Mapping of binary strings to their hexadecimal equivalents
    mappingHB = {
        "0000": '0', "0001": '1', "0010": '2', "0011": '3',
        "0100": '4', "0101": '5', "0110": '6', "0111": '7',
        "1000": '8', "1001": '9', "1010": 'A', "1011": 'B',
        "1100": 'C', "1101": 'D', "1110": 'E', "1111": 'F'
    }
    
    # Initialize an empty string to store the hexadecimal representation
    toHexadecimal = ""
    
    # Iterate over each 4-character block in the input binary string
    for i in range(0, len(input), 4):
        # Extract the current 4-character block
        ch = ""
        ch = ch + input[i]
        ch = ch + input[i + 1]
        ch = ch + input[i + 2]
        ch = ch + input[i + 3]
        
        # Append the hexadecimal equivalent of the current block to the result string
        toHexadecimal = toHexadecimal + mappingHB[ch]
    
    # Return the hexadecimal string
    return toHexadecimal


# Function to convert a binary string to a decimal integer
def binaryToDecimal(binary):
    # Initialize variables to store the decimal result and the current power of 2
    decimal, i, n = 0, 0, 0
    
    # Iterate over each character in the input binary string
    while(binary != 0):
        # Extract the current binary digit
        dec = binary % 10
        
        # Calculate the decimal equivalent of the current digit
        decimal = decimal + dec * pow(2, i)
        
        # Update the binary string and the power of 2
        binary = binary//10
        i += 1
    
    # Return the decimal integer
    return decimal


# Function to convert a decimal integer to a binary string
def decimalToBinary(num):
    # Convert the decimal integer to a binary string using the built-in bin function
    res = bin(num).replace("0b", "")
    
    # Pad the binary string with leading zeros to make its length a multiple of 4
    if(len(res) % 4 != 0):
        div = len(res) / 4
        div = int(div)
        counter = (4 * (div + 1)) - len(res)
        for i in range(0, counter):
            res = '0' + res
    
    # Return the binary string
    return res
# Function to perform a permutation operation on a binary string
def permutFunction(input, tables, toSize):
    # Initialize an empty string to store the permuted result
    permutation = ""
    
    # Iterate over each index in the permutation table
    for i in range(0, toSize):
        # Append the character at the current index in the input string to the result string
        permutation = permutation + input[tables[i] - 1]
    
    # Return the permuted string
    return permutation


# Function to perform a left shift operation on a binary string
def leftTextShiftOperation(input, noShifts):
    # Initialize an empty string to store the shifted result
    shiftSS = ""
    
    # Perform the specified number of left shifts
    for i in range(noShifts):
        # Shift the input string one position to the left
        for j in range(1, len(input)):
            shiftSS = shiftSS + input[j]
        shiftSS = shiftSS + input[0]
        
        # Update the input string for the next iteration
        input = shiftSS
        shiftSS = ""
    
    # Return the shifted string
    return input


# Function to perform an XOR operation on two binary strings
def xOrOperation(input1, input2):
    # Initialize an empty string to store the XOR result
    xOrInput = ""
    
    # Iterate over each character in the input strings
    for i in range(len(input1)):
        # Perform the XOR operation on the current characters
        if input1[i] == input2[i]:
            xOrInput = xOrInput + "0"
        else:
            xOrInput = xOrInput + "1"
    
    # Return the XOR result
    return xOrInput


# Function to encrypt a message using the DES algorithm
def encryptDESMessage(PlainText, roundKeys, avalenceX):
    # Convert the plaintext to a binary string
    PlainText = hexToBinary(PlainText)
    
    # Perform the initial permutation on the plaintext
    PlainText = permutFunction(PlainText, initialPermutationTable, 64)
    if not avalenceX:
        print("After initial permutation: ", binaryToHex(PlainText))

    # Split the plaintext into left and right halves
    leftText = PlainText[0:32]
    rightText = PlainText[32:64]
    if not avalenceX:
        print("After Splitting: ", "L0=", binaryToHex(leftText), "   R0=", binaryToHex(rightText))
        print()
        print("----------------------------------------------------------")
        print("ROUND", "    LEFT", "    RIGHT", "     ROUND KEYS")

    # Initialize a list to store the avalanche effect (if required)
    if avalenceX:
        avalenceXLS = []

    # Perform the 16 rounds of the DES algorithm
    for i in range(0, 16):
        # Expand the right half of the plaintext
        expRightText = permutFunction(rightText, expansionTable, 48)
        
        # Perform the XOR operation with the current round key
        xOrText = xOrOperation(expRightText, roundKeys[i])

        # Initialize an empty string to store the S-box output
        sBoxesText = ""
        
        # Iterate over each S-box
        for j in range(0, 8):
            # Calculate the row and column indices for the current S-box
            row = binaryToDecimal(int(xOrText[j * 6] + xOrText[j * 6 + 5]))
            col = binaryToDecimal(int(xOrText[j * 6 + 1] + xOrText[j * 6 + 2] + xOrText[j * 6 + 3] + xOrText[j * 6 + 4]))
            
            # Get the output of the current S-box
            val = sBoxes[j][row][col]
            sBoxesText = sBoxesText + decimalToBinary(val)

        # Perform the permutation on the S-box output
        sBoxesText = permutFunction(sBoxesText, permutationTable, 32)

        # Perform the XOR operation with the left half of the plaintext
        result = xOrOperation(leftText, sBoxesText)
        leftText = result

        # Swap the left and right halves (except for the last round)
        if(i != 15):
            leftText, rightText = rightText, leftText
        
        # Print the current round's output (if required)
        if not avalenceX:
            print(i + 1, "   ", binaryToHex(leftText), "   ", binaryToHex(rightText), "   ", binaryToHex(roundKeys[i]))
        
        # Store the avalanche effect (if required)
        if avalenceX:
            avalenceXLS.append(leftText+rightText)

    # Merge the left and right halves
    mergeText = leftText + rightText

    # Perform the final permutation on the merged text
    cipherText = permutFunction(mergeText , finalPermutationTable, 64)
    
    # Return the encrypted ciphertext (and the avalanche effect, if required)
    if avalenceX:
        return cipherText, avalenceXLS
    else:
        return cipherText
    
# Function to generate round keys from a given key
def generateRoundKeys(key):
    # Split the key into left and right halves
    leftText = key[:28]
    rightText = key[28:] 
    roundKeys = []
    
    # Iterate over each round
    for i in range(0, 16):
        # Perform a left shift operation on the left and right halves
        leftText = leftTextShiftOperation(leftText, keyScheduleShifts[i])
        rightText = leftTextShiftOperation(rightText, keyScheduleShifts[i])
        
        # Merge the left and right halves
        mergeText_str = leftText + rightText
        
        # Perform a permutation operation on the merged text
        round_key = permutFunction(mergeText_str, keyScheduleTable, 48)
        
        # Add the round key to the list of round keys
        roundKeys.append(round_key)
        
    # Return the list of round keys
    return roundKeys


def main1():
    # Define the plaintext and key
    PlainText = "123456ABCD132536"
    key = "AABB09182736CCDD"

    # Convert the key to binary
    key = hexToBinary(key)

    # Perform a permutation operation on the key
    key = permutFunction(key, keyPermutationTable, 56)
    
    # Generate the round keys
    roundKeys = generateRoundKeys(key=key)

    # Encrypt the plaintext using the DES algorithm
    print("")
    cipherText = encryptDESMessage(PlainText, roundKeys, avalenceX=False)
    cipherText = binaryToHex(cipherText)
    print()
    print("Cipher Text: ", cipherText, "(After final permutation)")


def count_bit_differences(str1, str2):
    # Count the number of bit differences between two strings
    return sum(ch1 != ch2 for ch1, ch2 in zip(str1, str2))


def calculate_bit_differences(round_outputs1, round_outputs2):
    # Calculate the bit differences for each round
    return [count_bit_differences(o1, o2) for o1, o2 in zip(round_outputs1, round_outputs2)]


def print_avalanche_output(plaintext1, ciphertext1, plaintext2, ciphertext2, bit_differences):
    # Print the avalanche output
    print("====================================")
    print("          Avalanche Output")
    print("====================================")
    print(f"Plaintext 1: {plaintext1}")
    print(f"Ciphertext 1: {binaryToHex(ciphertext1)}\n")
    
    print(f"Plaintext 2: {plaintext2}")
    print(f"Ciphertext 2: {binaryToHex(ciphertext2)}\n")
    
    print("Rounds:            ", end="")
    for i in range(1, 17):
        print(f"{i:2}   ", end="")
    print()
    print("Bit differences:   ", end="")
    for diff in bit_differences:
        print(f"{diff:2}   ", end="")
    print()
    print("====================================")


def main2():
    # Define the plaintexts and key
    plaintext1 = "0000000000000000"  # Initial plaintext
    plaintext2 = "0000000000000001"  # Changed plaintext
    key = "22234512987ABB23"  # Key
    key = hexToBinary(key)
    key = permutFunction(key, keyPermutationTable, 56)
    roundKey1 = generateRoundKeys(key)
    
    # Example round outputs (replace with actual DES round outputs)
    
    ciphertext1, round_outputs1 = encryptDESMessage(plaintext1, roundKey1, avalenceX=True)
    ciphertext2, round_outputs2 = encryptDESMessage(plaintext2, roundKey1, avalenceX=True)
    
    # Calculate bit differences for each round
    bit_differences = calculate_bit_differences(round_outputs1, round_outputs2)

    # Print the avalanche output
    print_avalanche_output(plaintext1, ciphertext1, plaintext2, ciphertext2, bit_differences)

if __name__ == "__main__":
    main1()
    main2()