# Advanced Buffer Overflow Demonstration

This repository contains two vulnerable TCP server implementations that demonstrate buffer overflow attacks with different security protections.

## Files Included

- `tcpserver-basic.c`: TCP server with executable stack (vulnerable to basic buffer overflow)
- `tcpserver-nonexecstack.c`: TCP server with non-executable stack (requires ROP exploitation)
- `exploitShellCode.py`: Example exploit script for the basic server

## Compilation Instructions

### Basic Server (Executable Stack)

```bash
gcc -o tcpserver-basic tcpserver-basic.c -fno-stack-protector -z execstack
```

This disables both stack canaries and enables executable stack, making it vulnerable to direct shellcode injection.

### Non-Executable Stack Server

```bash
gcc -o tcpserver-nonexecstack tcpserver-nonexecstack.c -fno-stack-protector
```

This disables stack canaries but keeps the non-executable stack protection, requiring ROP techniques.

## Running the Servers

```bash
# Disable ASLR first (as root)
echo 0 > /proc/sys/kernel/randomize_va_space

# Run basic server
./tcpserver-basic [port]

# Run non-executable stack server
./tcpserver-nonexecstack [port]
```

If no port is specified, the basic server uses port 9999 and the non-executable stack server uses port 9998.

## Vulnerability Explanation

Both servers contain a buffer overflow vulnerability in the `handle_client()` function:

```c
/* Receive data from client - VULNERABLE: no size checking */
bytes_received = recv(client_sock, buffer, 1024, 0);  // Deliberately receiving more than buffer size
```

The buffer is only 128 bytes, but the server tries to receive up to 1024 bytes, allowing an attacker to overflow the buffer and overwrite the return address.

## Exploitation Techniques

### Basic Server (Executable Stack)

The basic server can be exploited using traditional shellcode injection:
1. Overflow the buffer with a NOP sled
2. Append shellcode
3. Overwrite the return address to point to the NOP sled
4. When the function returns, execution jumps to the shellcode

### Non-Executable Stack Server

The non-executable stack server requires Return-Oriented Programming (ROP):
1. Overflow the buffer
2. Instead of shellcode, create a chain of addresses pointing to existing code fragments ("gadgets")
3. Chain these gadgets to execute system calls
4. The server includes dummy functions with useful gadgets for educational purposes

## Security Considerations

These programs are deliberately vulnerable and should only be used for educational purposes in a controlled environment. Never run these on production systems or networks.

## Advanced Exploitation

For the non-executable stack version, you'll need to:
1. Use the printed gadget addresses to build a ROP chain
2. Chain the gadgets to set up registers for an execve syscall
3. Execute the syscall using the int 0x80 gadget

This demonstrates how modern exploit mitigations can be bypassed with more sophisticated techniques.