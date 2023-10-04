#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

# Update package lists
sudo apt-get update

# Install nginx
sudo apt-get -y install nginx

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a simple HTML file as a test
echo "ALX SE" | sudo tee /data/web_static/releases/test/index.html

# Create a symbolic link to the "current" directory
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Change ownership of directories to the "ubuntu" user
sudo chown -R ubuntu:ubuntu /data/

# Add a configuration block to Nginx to serve static files
sudo sed -i "38i \\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default

# Restart Nginx to apply the configuration
sudo service nginx restart
