#!/bin/bash
# Install Nginx
sudo dnf install -y nginx

# Create file directory
sudo mkdir -p /var/www/files
sudo chmod 755 /var/www/files
sudo chown nginx:nginx /var/www/files

# Generate certificates
mkdir -p certs
openssl genrsa -out certs/ca.key 2048
openssl req -new -x509 -days 365 -key certs/ca.key -out certs/ca.crt -subj "/CN=Dummy CA"
openssl genrsa -out certs/server.key 2048
openssl req -new -key certs/server.key -out certs/server.csr -subj "/CN=localhost"
openssl x509 -req -days 365 -in certs/server.csr -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial -out certs/server.crt
openssl genrsa -out certs/reverse_proxy.key 2048
openssl req -new -key certs/reverse_proxy.key -out certs/reverse_proxy.csr -subj "/CN=localhost"
openssl x509 -req -days 365 -in certs/reverse_proxy.csr -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial -out certs/reverse_proxy.crt

# Configure Nginx
cat << EOF | sudo tee /etc/nginx/conf.d/files.conf
server {
    listen 443 ssl;
    server_name localhost;
    ssl_certificate /path/to/certs/server.crt;
    ssl_certificate_key /path/to/certs/server.key;
    root /var/www/files;
    autoindex on;
    location / {
        try_files \$uri \$uri/ =404;
    }
    location ~* ^/(.+)\$ {
        dav_methods PUT DELETE;
        create_full_put_path on;
        dav_access user:rw group:rw all:r;
    }
}
EOF

# Update certificate paths in Nginx config
sudo sed -i "s|/path/to/certs|$(pwd)/certs|g" /etc/nginx/conf.d/files.conf

# Start Nginx
sudo systemctl enable nginx
sudo systemctl start nginx