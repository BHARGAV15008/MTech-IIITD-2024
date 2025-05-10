#!/bin/bash

# Create the certs directory if it doesn't exist
mkdir -p certs

# Step 1: Create a Dummy CA
# Generate CA private key
openssl genrsa -out certs/ca.key 2048
# Generate CA certificate
openssl req -x509 -new -nodes -key certs/ca.key -sha256 -days 365 -out certs/ca.crt -subj "/C=US/ST=State/L=City/O=Organization/CN=CA"

# Step 2: Create Server Certificates
# Generate server private key
openssl genrsa -out certs/server.key 2048
# Generate server CSR
openssl req -new -key certs/server.key -out server.csr -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
# Sign server CSR with CA
openssl x509 -req -in server.csr -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial -out certs/server.crt -days 365 -sha256
# Remove temporary server CSR
rm server.csr

# Step 3: Create Reverse Proxy Certificates
# Generate reverse proxy private key
openssl genrsa -out certs/reverse_proxy.key 2048
# Generate reverse proxy CSR
openssl req -new -key certs/reverse_proxy.key -out reverse_proxy.csr -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
# Sign reverse proxy CSR with CA
openssl x509 -req -in reverse_proxy.csr -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial -out certs/reverse_proxy.crt -days 365 -sha256
# Remove temporary reverse proxy CSR
rm reverse_proxy.csr

echo "Certificates and keys have been generated in the certs/ directory:"
ls -l certs/