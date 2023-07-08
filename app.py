from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import sqlite3
import os

app = Flask(__name__)
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
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO objects (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    return 'Object added successfully!'

@app.route('/update/<int:object_id>', methods=['POST'])
def update_object(object_id):
    updated_data = request.get_json()
    name = updated_data['name']

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('UPDATE objects SET name=? WHERE id=?', (name, object_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Object updated successfully'})

@app.route('/delete/<int:object_id>', methods=['POST'])
def delete_object(object_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM objects WHERE id=?', (object_id,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Object deleted successfully'})

""" # utilizzo solo per prova su nginx
if __name__ == '__main__':
    create_table()
    app.run(host='localhost', port=0, debug=True) """



# Utilizzo nel caso generale
if __name__ == '__main__':
    create_table()
    app.run(host='0.0.0.0', port=0, debug=True)

    # Retrieve the actual port assigned by Flask
    assigned_port = app.config['SNIKSOCKET'].getsockname()[1]

    # Write the assigned port to a file
    with open('port.txt', 'w') as f:
        f.write(str(assigned_port))

    # Execute the script to update the Nginx configuration
    os.system('./update_nginx_config.sh')