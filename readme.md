 In data 22/7/23 - è stato impostato il flusso git tra vsc, droplet digitalocean and GH
 Here's a breakdown of the files and their purpose in the web calculator example:

app.py:

This file contains the Flask application code. It imports the Flask module and creates a Flask application instance. The @app.route('/') decorator defines a route for the root URL ("/") and associates it with the calculator() function. The calculator() function renders the index.html template. The @app.route('/function1') and @app.route('/function2') decorators define routes for the "/function1" and "/function2" URLs, respectively, and associate them with the function1() and function2() functions. The function1() and function2() functions are example functions that perform calculations and return the results as strings. Finally, the if name == 'main': block starts the Flask development server when the script is executed directly. index.html:

This file contains the HTML structure for the calculator. It includes a title, a heading, and two buttons with IDs "function1" and "function2". The CSS styles are linked using the tag. The JavaScript code is linked using the <script> tag. styles.css:

This file contains the CSS styles for the calculator. It includes styles for the body, heading, and buttons to give the calculator a centered layout and appropriate styling. script.js:

This file contains the JavaScript code that handles button clicks and performs AJAX requests. It listens for the "DOMContentLoaded" event, which ensures that the JavaScript code is executed after the HTML has been fully loaded. Inside the event listener, it retrieves the button elements with the IDs "function1" and "function2". The addEventListener() method is used to attach click event listeners to the buttons. When a button is clicked, an AJAX request is made to the corresponding route ("/function1" or "/function2") using the Fetch API. The response is processed, and an alert is displayed with the result.

GIT To push your Visual Studio Code (VSC) project to a GitHub repository, you can follow these steps:

Create a new repository on GitHub:

Go to the GitHub website and sign in to your account. Click on the "+" icon in the top-right corner and select "New repository". Give your repository a name, optionally add a description, choose if it should be public or private, and click "Create repository". Initialize Git in your VSC project:

Open a terminal in VSC by going to the View menu and selecting "Terminal". Navigate to your project directory using the cd command. Initialize Git in your project directory by running the command: shell Copy code git init Add your project files to the Git repository:

Add all the files in your project to the Git repository by running the command: shell Copy code git add . Commit your changes:

Create a commit to save the current state of your project by running the command: shell Copy code git commit -m "Initial commit" Replace "Initial commit" with an appropriate commit message that describes the changes you made. Connect your local repository to the GitHub repository:

On the GitHub repository page, copy the repository's remote URL. In the terminal, run the following command to add the remote repository: shell Copy code git remote add origin Replace with the URL you copied from the GitHub repository. Push your changes to the remote repository:

Run the following command to push your local changes to the remote repository: shell Copy code git push -u origin master This command pushes the changes to the master branch. If you're working with a different branch, replace master with the appropriate branch name. Enter your GitHub credentials:

When prompted, enter your GitHub username and password or personal access token to authenticate and push the changes. After completing these steps, your VSC project will be pushed to the GitHub repository. You can visit your repository on GitHub to verify that the files have been successfully uploaded.

To remember: The command git branch -M main is used to rename the default branch of a Git repository from the previous name (e.g., "master") to a new name (e.g., "main"). This command is typically used to align with more inclusive and neutral terminology.

Here's what each part of the command does:

git branch: This is the command to manage branches in Git. -M: This is an option that specifies the mode for renaming the branch. main: This is the new name for the branch. In this case, "main" is used as an example, but you can replace it with any desired branch name. By executing git branch -M main, you are effectively renaming the default branch of your Git repository to "main". This command ensures that the new branch name is updated in both your local repository and the remote repository.

The command git push -u origin main is used to push the local branch "main" to the remote repository named "origin" and set it as the upstream branch.

Here's what each part of the command does:

git push: This is the command to send your local commits to a remote repository. -u: This is an option that sets the upstream branch for the local branch being pushed. It tells Git to associate the local branch with the remote branch, enabling you to use git pull and git push without specifying the branch name in the future. origin: This is the remote repository's name. It is typically set as "origin" by default when you clone a repository. main: This is the branch you want to push to the remote repository. In this case, it is pushing the local branch "main" to the remote branch "main". By executing git push -u origin main, you are pushing the local branch "main" to the remote repository and setting it as the upstream branch. This allows you to use git pull and git push without specifying the branch name in subsequent commands.

One of the most important thisng - not present in this code is the file relative to Nginx proxy and reverse proxy server. So yer you are the file of /etc/nginx/nginx.con:

user www-data; worker_processes auto; pid /run/nginx.pid; include /etc/nginx/modules-enabled/*.conf;

events { worker_connections 1024; # multi_accept on; }

http {

##
# Basic Settings
##

sendfile on;
tcp_nopush on;
tcp_nodelay on;
keepalive_timeout 65;
types_hash_max_size 2048;
# server_tokens off;

# server_names_hash_bucket_size 64;
# server_name_in_redirect off;

include /etc/nginx/mime.types;
default_type application/octet-stream;

##
# SSL Settings
##

ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3; # Dropping SSLv3, ref: POODLE
ssl_prefer_server_ciphers on;

##
# Logging Settings
##

access_log /var/log/nginx/access.log;
error_log /var/log/nginx/error.log;

##
# Gzip Settings
##

gzip on;

# gzip_vary on;
# gzip_proxied any;
# gzip_comp_level 6;
# gzip_buffers 16 8k;
# gzip_http_version 1.1;
# gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

##
# Virtual Host Configs
##

include /etc/nginx/conf.d/*.conf;
include /etc/nginx/sites-enabled/*;

# Add server block for Flask application

server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://localhost:$http_port;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/flask_app/static;
    }
}
}

The above code is fully functional but the new code below is integrated with websocket (ed fully functional): user www-data; worker_processes auto; error_log /var/log/nginx/error.log; pid /var/run/nginx.pid;

events { worker_connections 1024; }

http { include /etc/nginx/mime.types; default_type application/octet-stream; log_format main '$remote_addr - $remote_user [$time_local] "$request" ' '$status $body_bytes_sent "$http_referer" ' '"$http_user_agent" "$http_x_forwarded_for"'; access_log /var/log/nginx/access.log main; sendfile on; keepalive_timeout 65;

##
# SSL Settings
##

ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;

##
# Gzip Settings
##

gzip on;
gzip_comp_level 4;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

##
# Virtual Host Configs
##

include /etc/nginx/conf.d/*.conf;
include /etc/nginx/sites-enabled/*;

# Add server block for Flask application

server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://localhost:$http_port;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/flask_app/static;
    }
}
}

To get into account also the https: address we extend the nnginx.conf to this:

user www-data; worker_processes auto; error_log /var/log/nginx/error.log; pid /var/run/nginx.pid;

events { worker_connections 1024; }

http { include /etc/nginx/mime.types; default_type application/octet-stream; log_format main '$remote_addr - $remote_user [$time_local] "$request" ' '$status $body_bytes_sent "$http_referer" ' '"$http_user_agent" "$http_x_forwarded_for"'; access_log /var/log/nginx/access.log main; sendfile on; keepalive_timeout 65;

##
# SSL Settings
##

ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;

##
# Gzip Settings
##

gzip on;
gzip_comp_level 4;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

##
# Virtual Host Configs
##

include /etc/nginx/conf.d/*.conf;
include /etc/nginx/sites-enabled/*;

# HTTP server block
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://localhost:$http_port;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/flask_app/static;
    }
}

# HTTPS server block
server {
    listen 443 ssl;
    server_name localhost;
    
    ssl_certificate /home/mauro/Scrivania/flask_server_2/certificate.crt;
    ssl_certificate_key /home/mauro/Scrivania/flask_server_2/ssl_certificate_key.key;

    location / {
        proxy_pass http://localhost:$http_port;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /path/to/flask_app/static;
    }
}
}

Attention this is the command to run to generate te 2 certificates: openssl req -x509 -newkey rsa:4096 -nodes -out /home/mauro/Scrivania/flask_server_2/ssl_certificate.crt -keyout /home/mauro/Scrivania/flask_server_2/ssl_certificate_key.key -days 365

There is problem to generate both http and https. So we have built a code with if then else statment If you want to account for both HTTP and HTTPS configurations without generating errors, you can modify the context parameter in the app.run() function to handle both cases. One approach is to use an if statement to conditionally set the ssl_context based on your desired configuration.

Here's an example of how you can modify the code to handle both HTTP and HTTPS configurations:

python Copy code if name == 'main': create_table()

# Check if HTTPS configuration is enabled
use_https = True  # Set this flag based on your configuration

if use_https:
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain('certificate.crt', 'ssl_certificate_key.key')
    app.run(host='0.0.0.0', port=0, debug=True, ssl_context=context)
else:
    app.run(host='0.0.0.0', port=0, debug=True)
In this modified code, the use_https flag is set to True if HTTPS configuration is desired, and False otherwise. Based on the value of this flag, the code conditionally sets the context variable and passes it to the ssl_context parameter of the app.run() function.

If use_https is True, the code sets up the SSL context and uses it for running the Flask app with HTTPS. If use_https is False, the code runs the Flask app without SSL.

By using this approach, you can handle both HTTP and HTTPS configurations without generating errors.
///-----////
questo è il nuovo flusso alle h. 20

#!/bin/bash

# Get the commit message as input
read -p "Enter the commit message: " commit_message

# Commit the changes
git add .
git commit -m "$commit_message"

# Define the branch name for the central repository
central_branch="vsc-repository-to-droplet"

# Pull changes from the remote vsc-repository-to-droplet branch on GitHub
echo "Pulling changes from origin/$central_branch"
git pull origin $central_branch

# Check if there are any conflicts after pulling
if [ $? -eq 0 ]; then
  # No conflicts, proceed with the push
  # Push changes to the GitHub repository
  echo "Pushing changes to origin/$central_branch"
  git push origin $central_branch

  # Log in to the DigitalOcean droplet and pull the changes
  echo "Logging in to the DigitalOcean droplet..."
  ssh root@146.190.169.21 "cd /home/mauro/flask-app && git pull"

  echo "Changes successfully pushed to both GitHub and the DigitalOcean droplet."
else
  # Conflicts exist, prompt the user to resolve them manually
  echo "There are conflicts after pulling. Please resolve the conflicts manually and commit the changes."
fi


//// h. 8:33 - Prova di inserimento di una nuova branch e sincronizzazione con Droplet e con GH ///
/// Posizionamento nuova branch anche su droplet
/// h. 10:22 - l'hook da l'opzione di lasciare la branch effettiva oppure cambiarla
/////////

Flusso che definisce le opzioni
#!/bin/bash

##

# Get the commit message as input
read -p "Enter the commit message: " commit_message

# Define the branch name for the central repository
central_branch="vsc-repository-to-droplet"

# Ask the user whether to create a new branch or remain on the current branch
read -p "Do you want to create a new branch? (y/n): " answer

if [[ $answer == "y" ]]; then
  # Get the name of the new branch from the user
  read -p "Enter the name of the new branch: " new_branch

  # Check if the local branch exists, if not, create it from the central branch
  if ! git show-ref --quiet refs/heads/$new_branch; then
    git checkout -b $new_branch $central_branch
  else
    git checkout $new_branch
  fi

  # Get the commit message for the new changes
  read -p "Enter the commit message for the new changes: " new_commit_message

  # Commit the changes on the new branch
  git add .
  git commit -m "$new_commit_message"

  # Push changes to the new local branch
  echo "Pushing changes to $new_branch"
  git push origin $new_branch

  # Switch to the new branch on the DigitalOcean droplet
  echo "Switching to the new branch on the DigitalOcean droplet..."
  ssh root@146.190.169.21 "cd /home/mauro/flask-app && git checkout $new_branch"
else
  # Commit the changes on the current branch
  git add .
  git commit -m "$commit_message"

  # Push changes to the current branch
  echo "Pushing changes to the current branch"
  git push origin $(git rev-parse --abbrev-ref HEAD)

  # Pull changes from the remote central branch on GitHub
  echo "Pulling changes from origin/$central_branch"
  git pull origin $central_branch

  # Check if there are any conflicts after pulling
  if [ $? -eq 0 ]; then
    # No conflicts, proceed with the push
    # Push changes to the GitHub repository
    echo "Pushing changes to origin/$central_branch"
    git push origin $central_branch

    # Log in to the DigitalOcean droplet and pull the changes
    echo "Logging in to the DigitalOcean droplet..."
    ssh root@146.190.169.21 "cd /home/mauro/flask-app && git pull"

    echo "Changes successfully pushed to both GitHub and the DigitalOcean droplet."
  else
    # Conflicts exist, prompt the user to resolve them manually
    echo "There are conflicts after pulling. Please resolve the conflicts manually and commit the changes."
  fi
fi
