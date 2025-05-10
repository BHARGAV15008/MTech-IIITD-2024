#!/bin/bash

# Create directories for certificates
mkdir -p certs
cd certs

# Generate CA private key
openssl genrsa -out ca.key 4096

# Generate CA certificate
openssl req -new -x509 -days 365 -key ca.key -out ca.crt -subj "/C=IN/ST=Delhi/L=Delhi/O=IIITD/OU=NSS/CN=CA"

# Generate server private key
openssl genrsa -out server.key 4096

# Generate server CSR
openssl req -new -key server.key -out server.csr -subj "/C=IN/ST=Delhi/L=Delhi/O=IIITD/OU=NSS/CN=server"

# Sign server certificate with CA
openssl x509 -req -days 365 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt

# Set appropriate permissions
chmod 600 *.key
chmod 644 *.crt *.csr

echo "Certificates generated successfully in the 'certs' directory"
echo "Please copy ca.crt to the client machine and server.crt, server.key to the server machine"