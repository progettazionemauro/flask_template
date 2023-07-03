from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

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

if __name__ == '__main__':
    create_table()
    app.run(port=0, debug=True)
