// Group Member: Ritesh Gupta (MT24132)

#include <iostream>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include <limits>


// Function to compute the Greatest Common Divisor (GCD) using the Euclidean algorithm
long long gcd(long long a, long long b) {
    // Base case: if b is 0, return a
    if (b == 0) 
        return a;
    // Recursive call with b and remainder of a divided by b
    return gcd(b, a % b);
}

// Function to compute (base^exponent) % modulus efficiently using modular exponentiation
long long mod_pow(long long base, long long exponent, long long modulus) {
    // If modulus is 1, return 0 (any number mod 1 is 0)
    if (modulus == 1) 
        return 0;
    
    long long result = 1; // Initialize result
    base = base % modulus; // Reduce base mod modulus
    
    // Loop until exponent becomes 0
    while (exponent > 0) {
        // If exponent is odd, multiply base with result
        if (exponent % 2 == 1)
            result = (result * base) % modulus;
        
        // Square the base
        base = (base * base) % modulus;
        exponent = exponent >> 1; // Divide exponent by 2
    }
    return result; // Return the final result
}

// Extended Euclidean Algorithm to find the modular multiplicative inverse of a under modulus m
long long mod_inverse(long long a, long long m) {
    long long m0 = m; // Store original modulus
    long long y = 0, x = 1; // Initialize x and y for the extended Euclidean algorithm
 
    if (m == 1) // If modulus is 1, return 0 (no inverse exists)
        return 0;
 
    // Apply extended Euclidean algorithm
    while (a > 1) {
        long long q = a / m; // Quotient
        long long t = m; // Store current modulus
 
        m = a % m; // Update m
        a = t; // Update a
        t = y; // Update y
 
        y = x - q * y; // Update y
        x = t; // Update x
    }
 
    // Make x positive
    if (x < 0)
        x += m0;
 
    return x; // Return the modular inverse
}

// Function to check if a number is prime
bool is_prime(long long n) {
    // Numbers <= 1 are not prime
    if (n <= 1) 
        return false;
    // 2 and 3 are prime numbers
    if (n <= 3) 
        return true;
    
    // Check divisibility by 2 and 3
    if (n % 2 == 0 || n % 3 == 0) 
        return false;
    
    // Check for factors from 5 to sqrt(n)
    for (long long i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0)
            return false; // Found a factor, not prime
    }
    return true; // No factors found, number is prime
}

// Function to clear the input buffer in case of invalid input
void clear_input_buffer() {
    std::cin.clear(); // Clear the error flag
    std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n'); // Ignore invalid input
}

// Class representing the ElGamal Digital Signature Scheme
class ElGamalSignature {
private:
    long long p;      // Large prime number
    long long alpha;  // Primitive root modulo p
    long long a;      // Private key
    long long beta;   // Public key (beta = alpha^a mod p)

public:
    // Constructor to initialize the keys to zero
    ElGamalSignature() : p(0), alpha(0), a(0), beta(0) {}

    // Check if alpha is a primitive root modulo p
    bool is_primitive_root(long long alpha, long long p) {
        // Alpha must be in the range (1, p)
        if (alpha <= 1 || alpha >= p) 
            return false;
        
        long long phi = p - 1; // Euler's totient function value for prime p
        
        // Check using all prime factors of p-1
        if (phi % 2 == 0) {
            if (mod_pow(alpha, phi / 2, p) == 1 ) 
                return false; // If alpha^(phi/2) ≡ 1 (mod p), alpha is not a primitive root
            phi /= 2; // Reduce phi
        }
        
        // Check for all odd factors of phi
        for (long long i = 3; i * i <= phi; i += 2) {
            if (phi % i == 0) {
                // If alpha^(phi/i) ≡ 1 (mod p), not a primitive root
                if (mod_pow(alpha, phi / i, p) == 1) 
                    return false; 
                while (phi % i == 0) 
                    phi /= i; // Remove factor i from phi
            }
        }
        // If phi is still greater than 1, check the last factor
        if (phi > 1) {
            // Check for the last factor
            if (mod_pow(alpha, (p - 1) / phi, p) == 1) 
                return false; 
        }
        
        return true; // Alpha is a primitive root
    }

    // Key Generation with user input validation
    bool generateKeys() {
        std::cout << "\n=== Key Generation ===\n";
        
        // Get prime number p from user
        while (true) {
            std::cout << "Enter a prime number p (e.g., 467): ";
            if (!(std::cin >> p)) { // Validate input
                std::cout << "Invalid input. Please enter a number.\n";
                clear_input_buffer(); // Clear invalid input
                continue; // Continue to next iteration
            }
            
            if (!is_prime(p)) { // Check if p is prime
                std::cout << "Error: " << p << " is not prime.\n";
                continue; // Continue to prompt for a valid prime
            }
            break; // Valid prime number entered
        }

        // Get primitive root alpha from user
        while (true) {
            std::cout << "Enter a primitive root alpha (e.g., 2): ";
            if (!(std::cin >> alpha)) { // Validate input
                std::cout << "Invalid input. Please enter a number.\n";
                clear_input_buffer(); // Clear invalid input
                continue; // Continue to next iteration
            }
            
            if (!is_primitive_root(alpha, p)) { // Check if alpha is a primitive root
                std::cout << "Error: " << alpha << " is not a primitive root modulo " << p << "\n";
                continue; // Continue to prompt for a valid primitive root
            }
            break; // Valid primitive root entered
        }
        
        int keyChoice; // Variable to store user's choice for key generation
        std::cout << "Choose key generation method: 1 for random key, 2 to enter your own: ";
        std::cin >> keyChoice; // Get user's choice
        if (keyChoice == 2) { // If user chooses to enter their own key
            std::cout << "Enter private key a (1 < a < " << p - 1 << "): ";
            std::cin >> a; // Get private key
            if (a <= 1 || a >= p - 1) { // Validate private key
                std::cout << "Invalid key. It must be between 1 and " << p - 1 << ".\n";
                return false; // Return false if invalid
            }
        } else {
            // Generate random private key a
            srand(time(0)); // Seed random number generator
            a = 2 + rand() % (p - 3); // Generate random private key in range (2, p-2)
        }
        
        // Calculate public key beta = alpha^a mod p
        beta = mod_pow(alpha, a, p);
        
        // Display generated keys
        std::cout << "\nKey Generation Successful!\n";
        std::cout << "Public Key (p, alpha, beta): " << p << ", " << alpha << ", " << beta << std::endl;
        std::cout << "Private Key (a): " << a << std::endl;
        
        return true; // Return true indicating successful key generation
    }
    
    // Signature Generation
    std::pair<long long, long long> sign(long long m) {
        // Validate message
        if (m < 0 || m >= p - 1) { 
            throw std::runtime_error("Message must be between 0 and p-2");
        }
        
        long long k; // Variable to store k
        int choice; // Variable to store user's choice for k generation
        std::cout << "Choose k generation method : 1 for random k, 2 to enter your own: ";
        std::cin >> choice; // Get user's choice for k generation
        if (choice == 2) { // If user chooses to enter their own k
            std::cout << "Enter k (1 < k < " << p - 1 << " and gcd(k, " << p - 1 << ") = 1): ";
            std::cin >> k; // Get k from user
            // Validate k: must be in range and coprime with p-1
            if (k <= 1 || k >= p - 1 || gcd(k, p - 1) != 1) { 
                throw std::runtime_error("Invalid k. It must be between 1 and " + std::to_string(p - 1) + " and gcd(k, " + std::to_string(p - 1) + ") = 1.");
            }
        } else {
            // Generate random k
            do {
                k = 2 + rand() % (p - 3); // Generate random k in range (2, p-2)
            } while (gcd(k, p - 1) != 1); // Ensure gcd(k, p-1) = 1
        }
        
        // Calculate signature components
        long long r = mod_pow(alpha, k, p); // r = alpha^k mod p
        long long k_inverse = mod_inverse(k, p - 1); // Calculate k's modular inverse
        long long s = (k_inverse * (m - a * r)) % (p - 1); // s = k_inverse * (m - a * r) mod (p-1)
        if (s < 0) s += (p - 1); // Ensure s is positive
        
        return std::make_pair(r, s); // Return the signature as a pair (r, s)
    }
    
    // Signature Verification
    bool verify(long long m, long long r, long long s) {
        // Validate r and s
        if (r <= 0 || r >= p || s <= 0 || s >= p - 1) { 
            return false; // Invalid signature components
        }
        
        // Calculate left side of the verification equation
        long long left = (mod_pow(beta, r, p) * mod_pow(r, s, p)) % p; // left = (beta^r * r^s) mod p
        long long right = mod_pow(alpha, m, p); // Calculate right side: right = alpha^m mod p
        
        return (left == right); // Return true if both sides are equal, indicating a valid signature
    }
    
    // Check if the ElGamal instance has been initialized
    bool is_initialized() const {
        return p != 0; // Return true if p is not zero, indicating keys have been generated
    }
};

// Function to print the menu options for the user
void print_menu() {
    std::cout << "\n=== ElGamal Digital Signature Menu ===\n";
    std::cout << "1. Generate New Keys\n"; // Option to generate new keys
    std::cout << "2. Sign a Message\n"; // Option to sign a message
    std::cout << "3. Verify a Signature\n"; // Option to verify a signature
    std::cout << "4. Exit\n"; // Option to exit the program
    std::cout << "Enter your choice (1-4): "; // Prompt for user input
}

int main() {
    ElGamalSignature elgamal; // Create an instance of the ElGamalSignature class
    int choice; // Variable to store user's menu choice
    
    std::cout << "Welcome to ElGamal Digital Signature System!\n"; // Welcome message
    
    while (true) { // Main loop for menu
        print_menu(); // Display menu options
        
        if (!(std::cin >> choice)) { // Validate user input
            std::cout << "Invalid input. Please enter a number.\n";
            clear_input_buffer(); // Clear invalid input
            continue; // Continue to the next iteration
        }
        
        try {
            switch (choice) { // Handle user choice
                case 1: { // Generate new keys
                    elgamal.generateKeys(); // Call key generation function
                    break; // Exit case
                }
                
                case 2: { // Sign a message
                    if (!elgamal.is_initialized()) { // Check if keys are generated
                        std::cout << "Please generate keys first (Option 1).\n";
                        break; // Exit case
                    }
                    
                    long long message; // Variable to store the message
                    std::cout << "\n=== Sign Message ===\n";
                    std::cout << "Enter the message (number): ";
                    if (!(std::cin >> message)) { // Validate message input
                        std::cout << "Invalid input. Please enter a number.\n";
                        clear_input_buffer(); // Clear invalid input
                        break; // Exit case
                    }
                    
                    // Call the sign function to generate the signature
                    auto signature = elgamal.sign(message);
                    std::cout << "Signature generated successfully!\n"; // Confirmation message
                    std::cout << "r = " << signature.first << "\n"; // Display r component of the signature
                    std::cout << "s = " << signature.second << "\n"; // Display s component of the signature
                    break; // Exit case
                }
                
                case 3: { // Verify a signature
                    if (!elgamal.is_initialized()) { // Check if keys are generated
                        std::cout << "Please generate keys first (Option 1).\n";
                        break; // Exit case
                    }
                    
                    long long m, r, s; // Variables to store message and signature components
                    std::cout << "\n=== Verify Signature ===\n";
                    std::cout << "Enter the message: ";
                    if (!(std::cin >> m)) { // Validate message input
                        std::cout << "Invalid input. Please enter a number.\n";
                        clear_input_buffer(); // Clear invalid input
                        break; // Exit case
                    }
                    
                    std::cout << "Enter signature component r: ";
                    if (!(std::cin >> r)) { // Validate r input
                        std::cout << "Invalid input. Please enter a number.\n";
                        clear_input_buffer(); // Clear invalid input
                        break; // Exit case
                    }
                    
                    std::cout << "Enter signature component s: ";
                    if (!(std::cin >> s)) { // Validate s input
                        std::cout << "Invalid input. Please enter a number.\n";
                        clear_input_buffer(); // Clear invalid input
                        break; // Exit case
                    }
                    
                    // Call verify function to check signature validity
                    bool is_valid = elgamal.verify(m, r, s);
                    std::cout << "\nSignature verification result: " 
                             << (is_valid ? "VALID" : "INVALID") << std::endl; // Display verification result
                    break; // Exit case
                }
                
                case 4: { // Exit the program
                    std::cout << "Thank you for using ElGamal Digital Signature System!\n"; // Exit message
                    return 0; // Exit the program
                }
                
                default: { // Handle invalid menu choice
                    std::cout << "Invalid choice. Please enter a number between 1 and 4.\n"; // Error message
                }
            }
        } catch (const std::exception& e) { // Catch any exceptions thrown during execution
            std::cerr << "Error: " << e.what() << std::endl; // Display error message
        }
    }
    
    return 0; // Return 0 indicating successful execution
}