import hmac  # Importing the HMAC module for generating HMAC digests
import itertools  # Importing itertools for generating combinations
import string  # Importing string for character manipulation
from random import SystemRandom  # Importing SystemRandom for secure random generation
from typing import Union  # Importing Union type for type hinting
import hashlib  # Importing hashlib module for hashing functions
from .HMAC_Algorithms import Hash_type_and_len  # Importing Hash_type_and_len dictionary from custom module
from .HMAC_Utils import to_bytes, to_str  # Importing utility functions for type conversions

# Secure random generation
random = SystemRandom()  # Creating an instance of SystemRandom for secure random number generation

class HMACClient:
    """
    HMAC (Hash-based Message Authentication Code) Client for message encryption and decryption.
    """

    def __init__(self, algorithm: str = 'sha3_256', secret: bytes = b"", symbol_count: int = 1):
        """
        Initialize the HMAC client with the given parameters.

        Parameters:
        - algorithm: The hashing algorithm to be used (default is 'sha3_256').
        - secret: The secret key for HMAC encryption (default is an empty byte string).
        """
        self._algorithm = algorithm  # Storing the hashing algorithm to be used
        self._secret = secret  # Storing the secret key for HMAC encryption
        self._decrypt_dict = {}  # Initializing a dictionary for decryption purposes
        self._symbol_count = symbol_count  # Storing the number of symbols per chunk
        self.init_decrypt_dict()  # Initializing the decryption dictionary

    def init_decrypt_dict(self) -> None:
        """
        Initialize the decryption dictionary with all possible combinations of characters.
        """
        all_chars = string.ascii_letters + string.digits + string.punctuation + " "  # Include spaces in characters

        combinations = itertools.product(all_chars, repeat=self._symbol_count)  # Generate all combinations

        for comb in combinations:
            value = ''.join(comb)  # Convert combination tuple to string
            key = self.encrypt_message(value)
            self._decrypt_dict[key] = value  # Store the encrypted value as key and original value as value

    def encrypt_message_by_chunks(self, message: str) -> str:
        """
        Encrypt a message by dividing it into chunks and encrypting each chunk.

        Parameters:
        - message: The message to be encrypted.

        Returns:
        - The encrypted message as a string.
        """
        message = to_bytes(message, 'utf-8')  # Ensure the message is encoded
        encrypted_message = ""  # Initialize encrypted message
        for i in range(0, len(message), self._symbol_count):  # Divide message into chunks
            chunk = message[i:i + self._symbol_count]  # Extract chunk
            encrypted_message += self.encrypt_message(chunk)  # Encrypt chunk
        return encrypted_message  # Return encrypted message

    def encrypt_message(self, message: Union[str, bytes]) -> str:
        """
        Encrypt a message using HMAC.

        Parameters:
        - message: The message to be encrypted.

        Returns:
        - The encrypted message as a string.
        """
        return hmac.new(self._secret, to_bytes(message, 'utf-8'),
                        self._algorithm).hexdigest()  # Generate HMAC digest

    def encrypt_message_digest(self, message: Union[str, bytes]) -> bytes:
        """
        Encrypt a message using HMAC.

        Parameters:
        - message: The message to be encrypted.

        Returns:
        - The encrypted message as bytes.
        """
        return hmac.new(self._secret, to_bytes(message, 'utf-8'),
                        self._algorithm).digest()  # Generate HMAC digest

    def decrypt_message_by_chunks(self, message: str, chank: None | int = None) -> Union[str, Exception]:
        """
        Decrypt a message by dividing it into chunks and decrypting each chunk.

        Parameters:
        - message: The message to be decrypted.
        - chank: The number of symbols in each chunk, or None to determine it from the algorithm.

        Returns:
        - The decrypted message as a string, or an exception if decryption fails.
        """
        if not chank:  # Use hash length if chunk size is not specified
            chank = Hash_type_and_len.get(self._algorithm, None)
            if not chank:
                raise ValueError(f"Unknown algorithm {self._algorithm}")
        
        if len(message) % chank != 0:  # Check message length alignment
            raise ValueError("Message length is not aligned with the chunk size.")

        msg_raw = ""  # Initialize decrypted message
        for i in range(0, len(message), chank):  # Divide encrypted message into chunks
            chunk = message[i:i + chank]  # Extract chunk
            msg_raw += self.decrypt_message(chunk)  # Decrypt chunk
        return msg_raw  # Return decrypted message

    def decrypt_message(self, message: str) -> Union[str, Exception]:
        """
        Decrypt a message using HMAC.

        Parameters:
        - message: The message to be decrypted.

        Returns:
        - The decrypted message as a string, or an exception if decryption fails.
        """
        val = self._decrypt_dict.get(message)  # Lookup chunk in the decryption dictionary
        if val:
            return val  # Return decrypted message if found
        else:
            raise ValueError(f"Decryption failed for chunk: {message}")  # Raise error for missing chunk
