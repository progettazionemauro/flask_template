#!/bin/bash

# Read the assigned port from port.txt
assigned_port=$(cat port.txt)

# Replace the placeholder in nginx.conf with the assigned port
sed -i "s/PORT_PLACEHOLDER/$assigned_port/" /etc/nginx/nginx.conf

# Start Gunicorn with the assigned port
# gunicorn app:app --bind 127.0.0.1:$assigned_port
sudo /home/mauro/Scrivania/flask_server_2/venv/bin/gunicorn app:app --bind 127.0.0.1:$assigned_port



# Restart Nginx
sudo service nginx restart
