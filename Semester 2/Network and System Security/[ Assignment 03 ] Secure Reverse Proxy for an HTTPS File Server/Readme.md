# Secure Reverse Proxy for HTTPS File Server

## Overview
This project implements a reverse proxy on Fedora (server) that interfaces with an HTTPS Nginx server for file operations, accessible from a FreeBSD client over TLS with PAM authentication. It fulfills the requirements of the Networks and Systems Security II (Winter 2025) Assignment 3.

## Assumptions
- Fedora hosts the reverse proxy and Nginx server.
- FreeBSD runs the client.
- Nginx serves files from `/var/uw/files`.
- Certificates are stored in `certs/` directory.
- System users on Fedora are used for PAM authentication.

## Setup Instructions
### Fedora (Server)
1. **Install Dependencies**:
   ```bash
   dnf install nginx openssl pam-devel gcc make pkgconf
   ```
2. **Generate Certificates**:
   ```bash
   chmod +x generate_certs.sh
   ./generate_certs.sh
   ```
   - Creates `ca.crt`, `reverse_proxy.crt`, `reverse_proxy.key`, `server.crt`, `server.key`, and CSRs.
3. **Configure Nginx**:
   - Copy `nginx.conf` to `/etc/nginx/nginx.conf`.
   - Update paths in `nginx.conf` to point to `certs/server.crt` and `certs/server.key`.
   - Create `/var/uw/files`:
     ```bash
     mkdir -p /var/uw/files
     chmod 755 /var/uw/files
     echo "Test file" > /var/uw/files/test.txt
     ```
   - Start Nginx:
     ```bash
     systemctl enable nginx
     systemctl start nginx
     ```
4. **Create Test User**:
   ```bash
   useradd -m testuser
   echo "testuser:password" | chpasswd
   ```
5. **Build**:
   ```bash
   make
   ```
6. **Run**:
   ```bash
   ./reverseProxy
   ```

### FreeBSD (Client)
1. **Install Dependencies**:
   ```bash
   pkg install openssl gcc pkgconf
   ```
2. **Copy Certificates**:
   - Copy `certs/ca.crt` from Fedora to FreeBSD’s `certs/` directory.
3. **Build**:
   ```bash
   make
   ```
4. **Run**:
   ```bash
   ./client <fedora_server_ip>
   ```

## Usage
- **Login**: Enter `testuser` and `password` at prompts.
- **Commands**:
  - `ls`: List files in `/var/uw/files`.
  - `get <filename>`: Download a file.
  - `put <filename> <size>`: Upload a file (enter `<size>` bytes).
  - `exit`: Terminate session.
- **Example**:
  ```
  Username: testuser
  Password: password
  HTTPS_SERVER> ls
  test.txt
  END
  HTTPS_SERVER> get test.txt
  OK 10
  HTTPS_SERVER> put newfile.txt 5
  Enter 5 bytes for newfile.txt: hello
  OK
  HTTPS_SERVER> exit
  ```

## Corner Cases
1. **TLS Handshake - Invalid Certificate**:
   - Test: Replace `certs/reverse_proxy.crt` with a certificate signed by a different CA. Run `./client <ip>`. Expect `SSL_connect failed` with `certificate verify failed`.
2. **TLS Handshake - Expired Certificate**:
   - Test: Generate an expired certificate (`-days 0`) and replace `reverse_proxy.crt`. Expect `SSL_connect failed` with `certificate expired`.
3. **PAM Authentication - Invalid Credentials**:
   - Test: Enter `wronguser` or incorrect password. Connection closes with `Login failed`.
4. **PAM Authentication - Empty Input**:
   - Test: Enter empty username or password. Server responds with `ERROR Invalid username/password` and closes connection.

## Test Cases
1. **Valid Login and Commands**:
   - Run `./client <ip>`, login, and test `ls`, `get test.txt`, `put newfile.txt 5`, `exit`.
2. **Invalid Credentials**:
   - Try incorrect username/password and verify connection closure.
3. **Invalid Certificate**:
   - Use Wireshark to capture failed TLS handshake with wrong CA certificate.
4. **Multiple Clients**:
   - Run multiple `./client <ip>` instances concurrently and verify independent sessions.

## Security Analysis
- **TLS**: Uses OpenSSL with `SSL_VERIFY_PEER` to ensure certificate validation.
- **PAM**: Authenticates against system users with `pam_start`, `pam_authenticate`, and `pam_acct_mgmt`.
- **Wireshark**: Capture successful handshake (client to proxy) and failed handshake (invalid certificate).

## Files
- `tlsClient.h`, `tlsClient.c`: TLS client setup.
- `tlsServer.h`, `tlsServer.c`: TLS server setup.
- `utils.h`, `utils.c`: Utility functions.
- `pamAuth.h`, `pamAuth.c`: PAM authentication.
- `httpClient.h`, `httpClient.c`: HTTP requests to Nginx.
- `reverseProxy.c`: Reverse proxy server.
- `client.c`: Client program.
- `Makefile`: Build script.
- `generate_certs.sh`: Certificate and CSR generation.
- `nginx.conf`: Nginx configuration.

## Notes
- Ensure `certs/` is in the working directory.
- Replace `/path/to/certs/` in `nginx.conf` with actual paths.
- Use Wireshark to capture TLS handshakes for submission.