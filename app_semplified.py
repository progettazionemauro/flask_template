from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import sqlite3
import os
import ssl
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with your own secret key

# Initialize the Flask-Login extension
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirect unauthorized users to the login page

# Define the path where the files will be stored on the server
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')  # Using 'uploads' folder inside the app's root path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

socketio = SocketIO(app)

DATABASE = 'database.db'

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv('.env')

# Create a User Model
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

# Replace this with your own user authentication logic
def authenticate_user(username, password):
    # Add your user authentication logic here
    # For demonstration purposes, we'll use a dummy username and password
    if username == 'demo_user' and password == 'demo_password':
        return User(user_id=1)  # For simplicity, we assume a single user with ID 1
    return None

@app.route('/hello-world')
@login_required
def hello_world():
    return render_template('hello-world.html')


# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    # Replace this with your code to load a user from the database or another data source
    # For this example, we'll assume there's a dictionary of users where the user ID is the key
    users = {
        1: User(1)  # Dummy user with ID 1 for demonstration
    }
    return users.get(int(user_id))

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS objects (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
    conn.commit()
    conn.close()
# OTHER ROUTES OF THE PROJECT
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))  # Redirect to the 'welcome' page if the user is already logged in

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)
        if user:
            login_user(user)
            return redirect(url_for('welcome'))
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('logout_landing_page'))

# Create a welcome page (protected with @login_required)
@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

# Render the logout landing page
@app.route('/logout-landing')
def logout_landing_page():
    return render_template('logout.html')


# Utilizzo nel caso generale
if __name__ == '__main__':
    create_table()

    # Check if HTTPS configuration is enabled
    use_https = False  # Set this flag based on your configuration

    if use_https:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        context.load_cert_chain('certificate.crt', 'ssl_certificate_key.key')
        socketio.run(app, host='0.0.0.0', port=0, debug=True, ssl_context=context)
    else:
        socketio.run(app, host='0.0.0.0', port=0, debug=True)
