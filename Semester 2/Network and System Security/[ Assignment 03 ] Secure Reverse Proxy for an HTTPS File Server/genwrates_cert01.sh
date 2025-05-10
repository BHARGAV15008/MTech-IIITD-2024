#!/bin/sh
mkdir -p certs
# Generate CA key and certificate
openssl genrsa -out certs/ca.key 2048
openssl req -x509 -new -nodes -key certs/ca.key -subj "/CN=Dummy CA" -days 365 -out certs/ca.crt

# Generate reverse proxy key and CSR
openssl genrsa -out certs/reverse_proxy.key 2048
openssl req -new -key certs/reverse_proxy.key -subj "/CN=reverse_proxy" -out certs/reverse_proxy.csr
openssl x509 -req -in certs/reverse_proxy.csr -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial -out certs/reverse_proxy.crt -days 365

# Generate backend server key and CSR
openssl genrsa -out certs/server.key 2048
openssl req -new -key certs/server.key -subj "/CN=localhost" -out certs/server.csr
openssl x509 -req -in certs/server.csr -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial -out certs/server.crt -days 365