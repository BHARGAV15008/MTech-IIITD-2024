# Zero-Knowledge Proofs for Authenticate and secure Communication Project

This project implements a communication system based on Zero-Knowledge Proofs (ZKP) and HMAC (Hash-based Message Authentication Code) for secure data transmission. The core idea is to allow one party (the prover) to convince another party (the verifier) that they possess certain information (like a secret key) without revealing the information itself. This README provides an overview of the project structure and explains how ZKP and HMAC work together to enhance security.

## Project Structure
```bash
F:\MTECH_IIITD\SEMESTER 1\APPLIED CRYPTOGRAPHY\ZKP-HMAC-COMMUNICATION-PYTHON
└───src
    ├───HMAC
    │   ├───algorithms
    │   ├───core
    │   ├───errors
    │   ├───types
    │   └───utils
    ├───SeedGeneration
    │   ├───core
    │   ├───errors
    │   ├───types
    │   └───utils
    └───ZeroKnowledge
        ├───algorithms
        ├───core
        ├───errors
        ├───models
        ├───types
        └───utils
```

### 1. `src`
The `src` folder is the main directory containing the source code for the project. It is divided into three main modules: `HMAC`, `SeedGeneration`, and `ZeroKnowledge`.

#### 1.1 `HMAC`
This module implements the HMAC functionality, which is used for message integrity and authentication. It is further divided into the following subfolders:

- **`algorithms`**: Contains different HMAC algorithms and their implementations. This may include various hashing functions such as SHA-256, SHA-512, etc.
  
- **`core`**: This folder contains the core logic and classes that manage HMAC operations. It may include the main classes for creating and verifying HMACs.
  
- **`errors`**: This folder defines custom error classes related to HMAC operations. It helps in managing exceptions and errors that may arise during the execution of HMAC functions.
  
- **`types`**: This folder contains type definitions and data structures used in the HMAC module. This could include classes for representing HMAC keys, messages, and other relevant data.
  
- **`utils`**: Utility functions that assist in HMAC operations. This may include functions for formatting data, converting between types, or other helper functions.

#### 1.2 `SeedGeneration`
This module is responsible for generating cryptographic seeds, which are essential for secure key generation and other cryptographic operations. It is divided into the following subfolders:

- **`core`**: Contains the main logic for seed generation, including algorithms and methods for generating secure random seeds.
  
- **`errors`**: Defines custom error classes related to seed generation, helping to manage exceptions that may occur during the seed generation process.
  
- **`types`**: Contains type definitions and data structures relevant to seed generation. This could include classes for representing seeds and configurations.
  
- **`utils`**: Utility functions that assist in seed generation tasks, such as random number generation or data formatting.

#### 1.3 `ZeroKnowledge`
This module implements the Zero-Knowledge Proofs (ZKP) functionality, which allows one party to prove to another that they know a value without revealing the value itself. It is structured into the following subfolders:

- **`algorithms`**: Contains various ZKP algorithms and their implementations. This may include protocols like Schnorr, Fiat-Shamir, etc.
  
- **`core`**: The core logic and classes that manage ZKP operations. This includes the main classes for creating and verifying zero-knowledge proofs.
  
- **`errors`**: Custom error classes related to ZKP operations, managing exceptions and errors that may arise during the execution of ZKP functions.
  
- **`models`**: Defines the data models used in ZKP processes. This could include classes for representing commitments, challenges, and responses in ZKP protocols.
  
- **`types`**: Type definitions and data structures relevant to the ZKP module, such as classes for cryptographic commitments and proof structures.
  
- **`utils`**: Utility functions that assist in ZKP operations , including functions for data encoding, proof generation, and verification processes.

## Overview of ZKP Communication with HMAC

### 1. Zero-Knowledge Proofs (ZKPs)
- **Definition**: ZKPs are cryptographic protocols that allow one party (the prover) to prove to another party (the verifier) that a statement is true without revealing any information beyond the validity of the statement.
- **Functionality**: This is particularly useful in scenarios where privacy is paramount, such as authentication processes, where the prover can demonstrate knowledge of a secret (like a password) without disclosing the secret itself.

### 2. Hash-based Message Authentication Code (HMAC)
- **Definition**: HMAC is a mechanism that combines a cryptographic hash function with a secret key to provide message integrity and authenticity.
- **Functionality**: By appending an HMAC to messages, both the sender and receiver can verify that the message has not been altered and that it comes from a legitimate source.

## Synergistic Operation
- **Combining ZKP and HMAC**: The integration of ZKPs with HMAC creates a robust framework for secure communication. While ZKPs ensure that sensitive information is not disclosed during the authentication process, HMAC guarantees that the messages exchanged are authentic and have not been tampered with.
- **Use Cases**: This combination is particularly beneficial in messaging applications, secure transactions, and any system requiring strong authentication without compromising user privacy.

## Core Components of the Project
### 1. Authentication Protocol
- **ZKP Mechanism**: The project implements a ZKP mechanism that allows users to authenticate themselves without revealing their credentials. This is achieved through cryptographic proofs that validate the user's identity.
- **HMAC for Message Integrity**: Each message sent between parties is accompanied by an HMAC, ensuring that the message has not been altered during transmission.

### 2. API Structure
- **ZeroKnowledge Class**: This class manages the creation and verification of ZKPs, handling the cryptographic operations required for the proof process.
- **HMACClient Class**: This class is responsible for generating HMACs for messages, providing methods for encrypting and decrypting messages securely.

### 3. Example Workflow
- **Client-Server Interaction**:
  - The client generates a ZKP to prove their identity to the server without revealing their password.
  - The server verifies the ZKP and responds with a token.
  - The client uses the token to generate a proof, which is sent back to the server.
  - The server verifies the proof and, if valid, allows further communication.
  - All messages exchanged are secured using HMAC to ensure integrity and authenticity.

## Benefits of the Project
- **Enhanced Security**: By using ZKPs, the project minimizes the risk of credential exposure, making it difficult for attackers to gain access to sensitive information.
- **Privacy Preservation**: Users can authenticate themselves without revealing their secrets, thus maintaining their privacy.
- **Integrity Assurance**: HMAC ensures that messages are not tampered with, providing a reliable communication channel.

## Conclusion
A project based on ZKP communication with HMAC represents a significant advancement in secure communication technologies. By leveraging the strengths of both ZKPs and HMAC, it provides a framework that not only protects user credentials but also ensures the integrity of the messages exchanged, making it suitable for various applications in today's digital landscape.