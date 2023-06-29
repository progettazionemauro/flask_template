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

if __name__ == '__main__':
    app.run(port=0)  # Use 0 to let the OS choose an available port
