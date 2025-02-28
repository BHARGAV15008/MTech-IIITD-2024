#!/bin/bash
# Define port for client and server communication
SERVER_PORT=12345
CLIENT_PORT=12346

# Define Files for saving and storing secrets of AES
PASSPHRASE_FILE="passphrase.txt"
IV_FILE="iv.txt"
KEY_FILE="aes.key"

# Capture Storing file
PCAP_FILE="trafficCapture.pcap"