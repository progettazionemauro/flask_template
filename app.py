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

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM objects')
    objects = cursor.fetchall()
    conn.close()
    return render_template('index.html', objects=objects)

@app.route('/add', methods=['POST'])
@login_required
def add_object():
    name = request.form['name']
    filename = None  # Initialize filename to None

    # Check if the post request has the file part
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            # Secure the filename to prevent malicious filenames
            filename = secure_filename(file.filename)
            # Save the file to the server
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO objects (name, filename) VALUES (?, ?)', (name, filename))  # Save the filename in the database
    conn.commit()
    conn.close()

    # Emit a socket event to notify clients about the newly created object
    socketio.emit('object_created', {'id': cursor.lastrowid, 'name': name, 'filename': filename})

    return 'Object added successfully!'


@app.route('/upload/<int:object_id>', methods=['POST'])
def upload_file(object_id):
    file = request.files['file']

    # Check if the post request has the file part
    if file:
        # Secure the filename to prevent malicious filenames
        # Secure the filename to prevent malicious filenames
        filename = secure_filename(file.filename)
        # Save the file to the server with the correct filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Update the filename in the database for the existing object
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('UPDATE objects SET filename=? WHERE id=?', (filename, object_id))  # Save the filename with extension
        conn.commit()
        conn.close()

        # Emit a socket event to notify clients about the successful file upload
        socketio.emit('file_uploaded', {'id': object_id, 'filename': filename})

        return 'File uploaded successfully!'

    return 'No file selected for upload.'


@app.route('/update/<int:object_id>', methods=['POST'])
def update_object(object_id):
    updated_data = request.get_json()
    name = updated_data['name']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE objects SET name=? WHERE id=?', (name, object_id))
    conn.commit()
    conn.close()

    # Emit a socket event to notify clients about the updated object
    socketio.emit('object_updated', {'id': object_id, 'name': name})

    return jsonify({'message': 'Object updated successfully'})

@app.route('/delete/<int:object_id>', methods=['POST'])
def delete_object(object_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT name, filename FROM objects WHERE id=?', (object_id,))
    row = cursor.fetchone()
    print(f"Row: {row}")  # Add this print statement to check the value of the row variable
    if row:
        name, filename = row  # Extract the name and filename from the database
        print(f"Name: {name}, Filename: {filename}")  # Add this print statement to check the values of name and filename
        cursor.execute('DELETE FROM objects WHERE id=?', (object_id,))
        conn.commit()
        conn.close()

        # Emit a socket event to notify clients about the deleted object
        socketio.emit('object_deleted', {'id': object_id, 'name': name})

        # Delete the associated file from the server
        if filename is not None:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"File '{filename}' deleted successfully.")
            else:
                print(f"File '{filename}' not found for deletion.")
        else:
            print("Filename is None, skipping deletion.")

        return jsonify({'message': 'Object deleted successfully'})

    conn.close()
    return jsonify({'message': 'Object not found'})

@app.route('/details/<int:object_id>', methods=['GET'])
def get_object_details(object_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM objects WHERE id=?', (object_id,))
    object_details = cursor.fetchone()
    conn.close()

    if object_details:
        # Assuming object_details contains (id, name, filename) from the database
        object_data = {
            'id': object_details[0],
            'name': object_details[1],
            'filename': object_details[2],
            # Add additional data fields as needed (e.g., date of review)
            'date_of_review': '2023-07-29'  # Replace this with the actual date of review from your database
        }
        return jsonify(object_data)

    return jsonify({'error': 'Object not found'})

@app.route('/details_page')
def object_details_page():
    # Retrieve the object details from the query parameters
    object_id = request.args.get('id')
    object_name = request.args.get('name')
    object_filename = request.args.get('filename')
    object_date_of_review = request.args.get('date_of_review')

    # Pass the object details as context variables to the 'details.html' template
    return render_template('details.html', object_id=object_id, object_name=object_name,
                           object_filename=object_filename, object_date_of_review=object_date_of_review)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)
        if user:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

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
