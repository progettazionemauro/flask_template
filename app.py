from function1 import function1
from function2 import function2
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def calculator():
    return render_template('index.html')

@app.route('/function1')
def function1_route():
    result = function1 ()
    return result

@app.route('/function2')
def function2_route():
    result = function2()
    return result
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
@app.route('/create_button', methods=['POST'])
def create_button():
    # Logic to handle the create button functionality
    button_id = request.form.get('button_id')

    # Create new button
    new_button = f'Button {button_id}'
    delete_button = f'Delete {button_id}'
    update_button = f'Update {button_id}'

    return {
        'new_button': new_button,
        'delete_button': delete_button,
        'update_button': update_button
    }

@app.route('/delete_button', methods=['POST'])
def delete_button():
    # Logic to handle the delete button functionality
    # You can access the button ID or any other necessary data from the request
    # Replace the code below with your own delete logic
    button_id = request.form.get('button_id')
    # Perform deletion operation based on the button_id

    return 'Button deleted successfully'  # Return an appropriate response

@app.route('/update_button', methods=['POST'])
def update_button():
    # Logic to handle the update button functionality
    # You can access the button ID or any other necessary data from the request
    # Replace the code below with your own update logic
    button_id = request.form.get('button_id')
    # Perform update operation based on the button_id

    return 'Button updated successfully'  # Return an appropriate response


if __name__ == '__main__':
    app.run(port=0)  # Use 0 to let the OS choose an available port
