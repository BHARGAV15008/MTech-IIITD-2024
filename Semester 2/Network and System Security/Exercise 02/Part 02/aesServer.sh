#!/bin/bash
# aesServer.sh - Improved AES server with proper connection handling

source aesConfig.sh

if [ ! -f "$KEY_FILE" ]; then
  echo "Error: Key file not found. Run genKey.sh first."
  exit 1
fi

KEY=$(cat "$KEY_FILE")

echo "Starting server on port $SERVER_PORT..."
echo "Press Ctrl+C to quit."

while true; do
  echo "Waiting for connection..."
  
  # Create a temporary file for the encrypted message
  enc_file=$(mktemp)
  
  # Receive the encrypted message
  nc -l $SERVER_PORT > "$enc_file"
  
  if [ ! -s "$enc_file" ]; then
    echo "Received empty data, continuing..."
    rm "$enc_file"
    continue
  fi
  
  echo "Received encrypted data."
  
  # Extract the client's listening port from the header
  client_port=$(grep "^RESPONSE_PORT:" "$enc_file" | cut -d':' -f2)
  if [ -z "$client_port" ]; then
    client_port=$CLIENT_PORT # Use default if not specified
  fi
  
  # Extract actual encrypted data (removing any headers)
  grep -v "^RESPONSE_PORT:" "$enc_file" > "${enc_file}.enc"
  
  # Decrypt the message using passphrase + key
  dec_file=$(mktemp)
  openssl enc -aes-256-cbc -d -base64 -salt -pbkdf2 -pass "pass:${PASSPHRASE}${KEY}" -in "${enc_file}.enc" -out "$dec_file" 2>/dev/null
  
  if [ $? -ne 0 ] || [ ! -s "$dec_file" ]; then
    echo "Error: Failed to decrypt the message."
    rm "$enc_file" "${enc_file}.enc" "$dec_file"
    continue
  fi
  
  # Get the decrypted message
  name=$(cat "$dec_file")
  echo "Decrypted message: '$name'"
  
  # Create response
  response="Hello $name!"
  echo "Response: '$response'"
  
  # Encrypt the response using passphrase + key
  resp_enc_file=$(mktemp)
  echo -n "$response" | openssl enc -aes-256-cbc -base64 -salt -pbkdf2 -pass "pass:${PASSPHRASE}${KEY}" -out "$resp_enc_file" 2>/dev/null
  
  if [ $? -ne 0 ]; then
    echo "Error: Failed to encrypt the response."
    rm "$enc_file" "${enc_file}.enc" "$dec_file" "$resp_enc_file"
    continue
  fi
  
  echo "Sending encrypted response to client port $client_port..."
  
  # Send the response to the client's listening port
  cat "$resp_enc_file" | nc localhost "$client_port"
  
  # Clean up temporary files
  rm "$enc_file" "${enc_file}.enc" "$dec_file" "$resp_enc_file"
  
  echo "Response sent."
done