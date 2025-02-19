# Group Member: Ritesh Gupta (MT24132)

class AESEncryption128:
    # Initialize various AES components
    sBox = list()  # Substitution box for the AES algorithm
    rCon = list()  # Round constants used in key expansion
    strRounds = list()  # Store the state after each round
    strSb = list()  # Store states after the SubBytes operation
    strSr = list()  # Store states after the ShiftRows operation
    strMc = list()  # Store states after the MixColumns operation
    strRk = list()  # Store the round keys used in each round


    def __init__(self):
        # sBox (Substitution Box) Initialize here
        self.sBox = [
            # 0     1     2     3     4     5     6     7     8     9     a     b     c     d     e     f
            0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76, # 0
            0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0, # 1
            0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15, # 2
            0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75, # 3
            0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84, # 4
            0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF, # 5
            0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8, # 6
            0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2, # 7
            0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73, # 8
            0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB, # 9
            0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79, # a
            0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08, # b
            0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A, # c
            0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E, # d
            0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF, # e
            0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16  # f
        ]

        # Initialize the round constants used in key expansion
        self.rCon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

    # Define XOR operation for bytes
    def xOrOperation(self, x, y): return x ^ y

    # Key expansion routine to generate round keys
    def keyExpansion(self, key):
        key_size = 16  # AES key size in bytes
        roundKeys = [0] * 176  # Prepare space for 11 round keys of 16 bytes each
        for i in range(key_size):
            roundKeys[i] = key[i]  # Copy the original key to the round keys
        
        # Generate the remaining round keys
        for i in range(4, 44):  # 44 = 11 * 4
            temp = roundKeys[(i - 1) * 4:i * 4]  # Get the previous key
            if i % 4 == 0:  # Apply specific operation every 4th key
                temp = self._keyScheduling(temp, i // 4)  # Key schedule operation
            roundKeys[i * 4:(i + 1) * 4] = [
                self.xOrOperation(roundKeys[(i - 4) * 4 + j], temp[j]) for j in range(4)
            ]
        
        return roundKeys

    # Key schedule operation: Rotate, Substitute, and XOR with rCon
    def _keyScheduling(self, temp, round):
        temp = temp[1:] + temp[:1]  # Rotate
        temp = [self.sBox[b] for b in temp]  # Substitute using S-box
        temp[0] ^= self.rCon[round - 1]  # XOR the first byte with rCon
        return temp

    # Substitute bytes using the S-box
    def subBytes(self, state):
        return [[self.sBox[state[r][c]] for c in range(4)] for r in range(4)]

    # Shift rows in the state array
    def shiftRows(self, state):
        return [state[0]] + [state[r][i:] + state[r][:i] for r, i in enumerate(range(1, 4), start=1)]

    # Add the round key to the state using XOR
    def addRoundKeys(self, state, round_key):
        return [[self.xOrOperation(state[r][c], round_key[c * 4 + r]) for c in range(4)] for r in range(4)]

    # MixColumns operation for the state
    def mixColumns(self, state):
        # Helper function for Galois field multiplication
        def _gmul(x, y):
            p = 0
            while y:
                if y & 1:
                    p ^= x  # Bitwise XOR if the lowest bit of y is 1
                x <<= 1
                if x & 0x100:  # x exceeds 255
                    x ^= 0x1B  # Reduce by the AES polynomial
                y >>= 1
            return p % 256  # Ensure the output fits in a byte

        new_state = [[0] * 4 for _ in range(4)]
        # Galois field multiplication and adding the results
        for c in range(4):
            new_state[0][c] = _gmul(0x02, state[0][c]) ^ _gmul(0x03, state[1][c]) ^ state[2][c] ^ state[3][c]
            new_state[1][c] = state[0][c] ^ _gmul(0x02, state[1][c]) ^ _gmul(0x03, state[2][c]) ^ state[3][c]
            new_state[2][c] = state[0][c] ^ state[1][c] ^ _gmul(0x02, state[2][c]) ^ _gmul(0x03, state[3][c])
            new_state[3][c] = _gmul(0x03, state[0][c]) ^ state[1][c] ^ state[2][c] ^ _gmul(0x02, state[3][c])
        return new_state

    # Main encryption routine for plaintext
    def textEncryption(self, plainText, key, rounds=10):
        # Perform initial transformations
        roundKeys = self.keyExpansion(key)  # Generate round keys
        state = [[plainText[c * 4 + r] for c in range(4)] for r in range(4)]  # Convert plaintext to state
        self.strRounds.append(state)  # Log initial state
        state = self.addRoundKeys(state, roundKeys[:16])  # Initial AddRoundKey
        self.strRounds.append(state)
        self.strRk.append(roundKeys[:16])  # Log round key
        
        # Iterate through the rounds
        for rNum in range(1, rounds):
            state = self.subBytes(state)  # Apply SubBytes
            self.strSb.append(state)
            state = self.shiftRows(state)  # Apply ShiftRows
            self.strSr.append(state)
            if rNum < rounds:  # Avoid MixColumns on the final round
                state = self.mixColumns(state)  # Apply MixColumns
                self.strMc.append(state)
            roundKey = roundKeys[rNum * 16: (rNum + 1) * 16]  # Select the round key
            self.strRk.append(roundKey)  # Log round key
            state = self.addRoundKeys(state, roundKey)  # Add round key
            self.strRounds.append(state)  # Log state
            
        # Final round (without MixColumns)
        state = self.subBytes(state)
        self.strSb.append(state)
        state = self.shiftRows(state)
        self.strSr.append(state)
        roundKey = roundKeys[rounds * 16:]  # Last round key
        self.strRk.append(roundKey)
        state = self.addRoundKeys(state, roundKey)  # Final AddRoundKey
        self.strRounds.append(state)  # Log final state

        cipherText = [state[r][c] for c in range(4) for r in range(4)]  # Convert state to column-major format
        return cipherText

# Format output for printing 
def outputFormat(data):
    return ' '.join(f"{byte:02x}" for byte in data)

# Print state tables after each round of AES encryption
def printTable(strRounds, strSb, strSr, strMc, strRk, ro):
    """
    Print the state of the AES-like encryption process after each round.

    Parameters:
    - strRounds: List of rounds data.
    - strSb: List of data after SubBytes.
    - strSr: List of data after ShiftRows.
    - strMc: List of data after MixColumns.
    - strRk: List of round keys.
    """
    
    def print_hex_data(label, data, i):
        print(label, i)  # Print the label and round number
        if isinstance(data[0], list):  # Check if it's a nested list
            for sublist in data:  # For each sublist (i.e., each row of the state)
                hex_values = "   ".join(f"0x{num:02x}" for num in sublist)  # Print hex values
                print(hex_values)
        else:  # For flat data
            hex_values = "   ".join(f"0x{num:02x}" for num in data)
            print(hex_values)
        print()  # Newline for separation

    # Print the initial state before any rounds
    print_hex_data("Start of Rounds: ", strRounds[0], 0)
    print_hex_data("After Round Key: ", strRk[0], 0)

    print("==============================================================================")

    # Main loop through rounds
    labels = [
        "Start of Rounds: ",
        "After SubBytes: ",
        "After ShiftRows: ",
        "After MixColumns: ",
        "After Round Key: "
    ]
    print("List out all the Rounds and Respective their value: ")
    for j in range(1, 10):
        data = [strRounds[j], strSb[j-1], strSr[j-1], strMc[j-1], strRk[j]]  # Gather the data to print
        for i, item in enumerate(data):
            print_hex_data(labels[i], item, j)  # Print each stage of the round
            
        print("==============================================================================")

    # Print final round information
    data = [strRounds[10], strSb[9], strSr[9], strRk[10]]
    for i, item in enumerate(data):
        print_hex_data(labels[i], item, 10)

    print("==============================================================================")

    data = [strRounds[11]]  # Final state after all rounds
    for i, item in enumerate(data):
        print_hex_data(labels[i], item, 11)
    
    print("==============================================================================")

    print("==============================================================================")
    print("================  You have to show Round: ", ro, "============================")
    print("==============================================================================")
    if ro < 1:
        data = [strRounds[ro], strRk[ro]]
    elif ro >= 1 and ro <= 9:
        data = [strRounds[ro], strSb[ro-1], strSr[ro-1], strMc[ro-1], strRk[ro]]
    elif ro == 10:
        data = [strRounds[10], strSb[9], strSr[9], strRk[10]]
    elif ro == 11:
        data = [strRounds[11]]

    for i, item in enumerate(data):
        print_hex_data(labels[i], item, ro)



if __name__ == "__main__":
    inputPlainText = "0123456789abcdeffedcba9876543210"  # Example plaintext (32 hex characters = 16 bytes)
    inputKey = "0f1571c947d9e8590cb7add6af7f6798"  # Example key (32 hex characters = 16 bytes)

    # Convert string inputs to byte format for AES
    plainTextState = [int(inputPlainText[i:i + 2], 16) for i in range(0, len(inputPlainText), 2)]
    keyState = [int(inputKey[i:i + 2], 16) for i in range(0, len(inputKey), 2)]

    aes = AESEncryption128()  # Create an instance of the AES encryption class

    # Get the number of rounds from user input
    try:
        noRounds = int(input("Enter the number of rounds (1-10): "))  # Prompt for number of rounds
    except ValueError:
        print("Invalid input. Please enter an integer between 1 and 10.")  # Handle non-integer input
        exit()

    if noRounds < 1 or noRounds > 10:  # Validate number of rounds
        print("Invalid number of rounds. Please enter a number between 1 and 10.")
    else:
        cipherText = aes.textEncryption(plainTextState, keyState, 10)  # Encrypt the text
        printTable(aes.strRounds, aes.strSb, aes.strSr, aes.strMc, aes.strRk, noRounds)  # Print round tables
        formatCipher = outputFormat(cipherText)  # Format the cipher for output
        print(f"cipherText: {formatCipher}")  # Print the final ciphertext