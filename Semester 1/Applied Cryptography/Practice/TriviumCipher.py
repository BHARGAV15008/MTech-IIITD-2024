def bitstring_to_bytes(bitstring):
    """Convert a bitstring to bytes."""
    bitstring = bitstring.zfill(((len(bitstring) + 7) // 8) * 8)
    return int(bitstring, 2).to_bytes(len(bitstring) // 8, byteorder='big')

def bytes_to_bitstring(byte_data):
    """Convert bytes to a bitstring."""
    return ''.join(f'{byte:08b}' for byte in byte_data)

class Trivium:
    def __init__(self, key, iv):
        self.state = [0] * 288
        self.set_key_iv(key, iv)

    def set_key_iv(self, key, iv):
        # Set the key
        key_bits = f'{key:080b}'
        for i in range(80):
            self.state[i] = int(key_bits[i])
        # Set the IV
        iv_bits = f'{iv:080b}'
        for i in range(80):
            self.state[80 + i] = int(iv_bits[i])
        # Initialize the remaining bits to 1
        self.state[160:] = [1] * 128
        # Perform the key setup phase (updating the state)
        for _ in range(1152):
            self.generate_bit()

    def generate_bit(self):
        # Compute the bits used for generating the output
        t1 = self.state[65]
        t2 = self.state[92]
        t3 = self.state[161]
        t4 = self.state[172]
        t5 = self.state[253]
        t6 = self.state[284]

        # Compute the new bit
        new_bit = (t1 ^ t2) ^ (t3 ^ t4) ^ (t5 ^ t6)
        
        # Shift state and insert new bit
        self.state = [new_bit] + self.state[:-1]
        return new_bit

    def generate_keystream(self, length):
        keystream_bits = []
        for _ in range(length):
            keystream_bits.append(self.generate_bit())
        return keystream_bits

def keystream_to_hex(keystream_bits):
    bitstring = ''.join(map(str, keystream_bits))
    keystream_bytes = bitstring_to_bytes(bitstring)
    return keystream_bytes.hex().upper()

def main():
    # Test vectors
    test_vectors = [
        {'key': 0x80000000000000000000, 'iv': 0x00000000000000000000, 'expected_length': 512},
        {'key': 0x00400000000000000000, 'iv': 0x00000000000000000000, 'expected_length': 512},
        {'key': 0x00002000000000000000, 'iv': 0x00000000000000000000, 'expected_length': 512},
        {'key': 0x00000010000000000000, 'iv': 0x00000000000000000000, 'expected_length': 512},
        {'key': 0x00000000080000000000, 'iv': 0x00000000000000000000, 'expected_length': 512},
        {'key': 0x00000000000400000000, 'iv': 0x00000000000000000000, 'expected_length': 512},
        {'key': 0x00000000000002000000, 'iv': 0x00000000000000000000, 'expected_length': 512},
        {'key': 0x00000000000000010000, 'iv': 0x00000000000000000000, 'expected_length': 512},
        {'key': 0x00000000000000000080, 'iv': 0x00000000000000000000, 'expected_length': 512}
    ]

    for test in test_vectors:
        key = test['key']
        iv = test['iv']
        expected_length = test['expected_length']

        trivium = Trivium(key, iv)
        keystream_bits = trivium.generate_keystream(expected_length)
        keystream_hex = keystream_to_hex(keystream_bits)

        print(f'Key: {key:020X}')
        print(f'IV: {iv:020X}')
        print(f'Keystream: {keystream_hex}')

if __name__ == '__main__':
    main()
