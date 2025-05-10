# Buffer Overflow Exercise Solutions

This repository contains solutions for the buffer overflow exercise with two parts:
1. Basic buffer overflow exploit for `tcpserver-basic`
2. Return-Oriented Programming (ROP) exploit for `tcpserver-nonexecstack`

## Prerequisites

### Disable ASLR

Before running any of the exploits, you need to disable Address Space Layout Randomization (ASLR) on your Linux system:

```bash
echo 0 > /proc/sys/kernel/randomize_va_space
```

## Part 1: Basic Buffer Overflow (`exploit-basic.py`)

### Overview

The `tcpserver-basic` program has a buffer overflow vulnerability that allows us to inject shellcode and execute it. The exploit works by:

1. Creating a payload with a NOP sled
2. Adding shellcode that spawns a shell
3. Padding the buffer to reach the return address
4. Overwriting the return address to point to our shellcode

### Usage

1. Start the vulnerable server with a port number:

```bash
./tcpserver-basic 9999
```

2. Run the exploit script:

```bash
python3 exploit-basic.py
```

### Customization

You may need to adjust the following in `exploit-basic.py`:

- `target_port`: Change to match the port your server is running on
- `ret_addr`: The return address needs to be adjusted to point to your NOP sled

To find the correct return address, you can use GDB with pattern generation or trial and error with different addresses in the stack.

## Part 2: ROP Exploit (`exploit-rop.py`)

### Overview

The `tcpserver-nonexecstack` program has the same buffer overflow vulnerability but with non-executable stack protection (NX bit). This requires a more advanced Return-Oriented Programming (ROP) technique to bypass the protection.

The exploit works by:

1. Overflowing the buffer
2. Building a ROP chain that uses existing code fragments (gadgets) in the binary
3. Chaining these gadgets to execute system calls (specifically `execve("/bin/sh", NULL, NULL)`)

### Usage

1. Start the vulnerable server with a port number:

```bash
./tcpserver-nonexecstack 9999
```

2. Run the exploit script:

```bash
python3 exploit-rop.py
```

### Customization

Before using the ROP exploit, you **must** find the correct gadget addresses for your specific binary. The current addresses in the script are placeholders.

1. Install ROPgadget:

```bash
pip install ROPgadget
```

2. Find gadgets in your binary:

```bash
ROPgadget --binary tcpserver-nonexecstack
```

3. Update the following in `exploit-rop.py`:
   - Gadget addresses (`pop_rdi`, `pop_rsi`, `pop_rdx`, `pop_rax`, `syscall`)
   - Address of a "/bin/sh" string (you may need to add this to memory)
   - Buffer size and return address
   - Target port

## Debugging Tips

1. Use GDB to debug the server and find correct addresses:

```bash
gdb ./tcpserver-basic
```

2. Find the buffer size with pattern generation:

```bash
(gdb) pattern create 200
(gdb) run 9999
# Send the pattern to the server
(gdb) info registers
# Look at the EIP/RIP register value
(gdb) pattern offset <value>
```

3. Find gadget addresses with objdump:

```bash
objdump -d tcpserver-nonexecstack | grep -A1 "pop.*rdi" | grep ret
```

## Security Note

These exploits are for educational purposes only. The techniques demonstrated should only be used on systems you have permission to test.

## References

- [Smashing The Stack For Fun And Profit](http://phrack.org/issues/49/14.html)
- [ROP Emporium](https://ropemporium.com/)
- [Return-Oriented Programming: Systems, Languages, and Applications](https://cseweb.ucsd.edu/~hovav/dist/rop.pdf)