#!/bin/bash
# aesClient.sh - Improved AES client with proper connection handling

source aesConfig.sh

if [ ! -f "$KEY_FILE" ]; then
  echo "Error: Key file not found. Run genKey.sh first."
  exit 1
fi

KEY=$(cat "$KEY_FILE")

# Get input
echo -n "Enter your name: "
read name

echo "Encrypting: '$name'"

# Create temporary file for the message
msg_file=$(mktemp)
echo -n "$name" > "$msg_file"

# Encrypt the message using passphrase + key
enc_file=$(mktemp)
openssl enc -aes-256-cbc -base64 -salt -pbkdf2 -pass "pass:${PASSPHRASE}${KEY}" -in "$msg_file" -out "$enc_file" 2>/dev/null

if [ $? -ne 0 ]; then
  echo "Error: Failed to encrypt the message."
  rm "$msg_file" "$enc_file"
  exit 1
fi

echo "Sending encrypted data to server..."

# Start client listener for response BEFORE sending data
resp_file=$(mktemp)
nc -l $CLIENT_PORT > "$resp_file" &
nc_pid=$!

# Give the netcat listener a moment to start
sleep 1

# Send the encrypted data to the server with a header indicating which port to respond to
(echo "RESPONSE_PORT:$CLIENT_PORT"; cat "$enc_file") | nc localhost $SERVER_PORT

# Wait for response with timeout
timeout=10
count=0
while [ ! -s "$resp_file" ] && [ $count -lt $timeout ]; do
  sleep 1
  ((count++))
done

# Check if we got a response
if [ ! -s "$resp_file" ]; then
  echo "Error: No response received from server within $timeout seconds."
  kill $nc_pid 2>/dev/null
  rm "$msg_file" "$enc_file" "$resp_file"
  exit 1
fi

echo "Received encrypted response."

# Extract actual encrypted data (removing any headers)
grep -v "^RESPONSE_PORT:" "$resp_file" > "${resp_file}.enc"

# Decrypt the response using passphrase + key
dec_resp_file=$(mktemp)
openssl enc -aes-256-cbc -d -base64 -salt -pbkdf2 -pass "pass:${PASSPHRASE}${KEY}" -in "${resp_file}.enc" -out "$dec_resp_file" 2>/dev/null

if [ $? -ne 0 ]; then
  echo "Error: Failed to decrypt the server response."
  rm "$msg_file" "$enc_file" "$resp_file" "${resp_file}.enc" "$dec_resp_file"
  exit 1
fi

# Display the response
response=$(cat "$dec_resp_file")
echo "Server response: $response"

# Clean up temporary files
rm "$msg_file" "$enc_file" "$resp_file" "${resp_file}.enc" "$dec_resp_file"

