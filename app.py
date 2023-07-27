from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import sqlite3
import os
import ssl
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Replace with your own secret key

# Define the path where the files will be stored on the server
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')  # Using 'uploads' folder inside the app's root path
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

socketio = SocketIO(app)

DATABASE = 'database.db'

# Load environment variables from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv('.env')

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
        filename = secure_filename(file.filename)
        filename_without_extension = os.path.splitext(filename)[0]  # Get the filename without the extension
        # Save the file to the server with the correct filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_without_extension))

        # Update the filename in the database for the existing object
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('UPDATE objects SET filename=? WHERE id=?', (filename_without_extension, object_id))
        conn.commit()
        conn.close()

        # Emit a socket event to notify clients about the successful file upload
        socketio.emit('file_uploaded', {'id': object_id, 'filename': filename_without_extension})

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
