#!/bin/bash
# genSecrets.sh - Generates and saves the passphrase and initialization vector

source aesConfig.sh

echo "Generating cryptographic secrets..."

# Generate a simple fixed passphrase (for simplicity and reliability)
echo "bhargavispass" > "$PASSPHRASE_FILE"
chmod 600 "$PASSPHRASE_FILE"

# Generate a fixed IV (16 bytes for GCM mode)
openssl rand -hex 16 > "$IV_FILE"
chmod 600 "$IV_FILE"

echo "Generating AES key..."

# Generate a random 32-byte key (256 bits) for AES-256-GCM
openssl rand -hex 32 > "$KEY_FILE"
chmod 600 "$KEY_FILE"

echo "AES key generated successfully and saved to: $KEY_FILE"
echo "Key: $(cat $KEY_FILE)"
echo "Secrets generated successfully:"
echo "- Passphrase saved to: $PASSPHRASE_FILE (value: $(cat $PASSPHRASE_FILE))"
echo "- IV saved to: $IV_FILE (value: $(cat $IV_FILE))"