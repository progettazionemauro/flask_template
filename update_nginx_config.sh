#!/bin/bash

# Read the assigned port from port.txt
assigned_port=$(cat port.txt)

# Replace the placeholder in nginx.conf with the assigned port
sed -i "s/PORT_PLACEHOLDER/$assigned_port/" /etc/nginx/nginx.conf

# Restart Nginx
sudo service nginx restart
