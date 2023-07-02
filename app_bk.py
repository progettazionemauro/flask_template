# I dati dei bottoni vengono prcessati dinamicamente. Di seguito la spiegazione:
""" Route Definition:

@app.route('/create_button', methods=['POST'])
def create_button():
This route is defined to handle the /create_button URL and expects a POST request.
Retrieving Button ID:

    button_id = request.form.get('button_id')
The request.form.get('button_id') statement retrieves the value of the button_id from the form data of the POST request.
It assumes that the form data contains a field with the name button_id which holds the ID of the button being created.
Generating Button Text:

    new_button = f'Button {button_id}'
    delete_button = f'Delete {button_id}'
    update_button = f'Update {button_id}'
Three strings are generated using f-strings:
new_button: Represents the text for the newly created button. It includes the button_id in the format 'Button {button_id}'.
delete_button: Represents the text for the delete button associated with the newly created button. It includes the button_id in the format 'Delete {button_id}'.
update_button: Represents the text for the update button associated with the newly created button. It includes the button_id in the format 'Update {button_id}'.
Returning the Response:

    return {
        'new_button': new_button,
        'delete_button': delete_button,
        'update_button': update_button
    }
The response is returned as a dictionary object containing the three button texts (new_button, delete_button, update_button).
The response will be in JSON format, where each button text is associated with a corresponding key.
For example:

{
    "new_button": "Button 1",
    "delete_button": "Delete 1",
    "update_button": "Update 1"
}
This JSON response can be processed by the client-side code (JavaScript) to dynamically generate the buttons on the webpage. """
from flask import Flask, render_template, request, g
import sqlite3
from function1 import function1
from function2 import function2

app = Flask(__name__)
app.config['DATABASE'] = 'buttons.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db


def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS buttons (
                button_id INTEGER PRIMARY KEY,
                new_button TEXT NOT NULL,
                delete_button TEXT NOT NULL,
                update_button TEXT NOT NULL
            )
        ''')
        db.commit()


@app.route('/')
def calculator():
    return render_template('index.html')


@app.route('/function1')
def function1_route():
    result = function1()
    return result


@app.route('/function2')
def function2_route():
    result = function2()
    return result


@app.route('/create_button', methods=['POST'])
def create_button():
    if request.method == 'POST':
        with app.app_context():
            # Handle POST request logic to create a new button
            button_id = request.form.get('buttonId')  # Update to 'buttonId'
            print(f"Received button_id: {button_id}")  # Print the button_id for debugging

            new_button = f'Button {button_id}'
            delete_button = f'Delete {button_id}'
            update_button = f'Update {button_id}'

            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO buttons (button_id, new_button, delete_button, update_button) VALUES (?, ?, ?, ?)",
                (button_id, new_button, delete_button, update_button))
            db.commit()
            print("Button inserted successfully")

            return {
                'new_button': new_button,
                'delete_button': delete_button,
                'update_button': update_button
            }
    else:
        return 'Method not allowed'


@app.route('/delete_button', methods=['POST'])
def delete_button():
    if request.method == 'POST':
        with app.app_context():
            button_id = request.form.get('button_id')

            db = get_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM buttons WHERE button_id=?", (button_id,))
            db.commit()

            return 'Button deleted successfully'
    else:
        return 'Method not allowed'


@app.route('/update_button', methods=['POST'])
def update_button():
    if request.method == 'POST':
        with app.app_context():
            button_id = request.form.get('button_id')

            db = get_db()
            cursor = db.cursor()
            cursor.execute("UPDATE buttons SET new_button=?, delete_button=?, update_button=? WHERE button_id=?",
                           (f'Button {button_id}', f'Delete {button_id}', f'Update {button_id}', button_id))
            db.commit()

            return 'Button updated successfully'
    else:
        return 'Method not allowed'


@app.route('/get_buttons', methods=['GET'])
def get_buttons():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT button_id, new_button, delete_button, update_button FROM buttons")
        buttons = cursor.fetchall()

        return {
            'buttons': buttons
        }


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(port=0, debug=True)
