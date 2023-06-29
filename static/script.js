// This code sets up an event listener on the mouseup event of the document. 
// When the user releases the mouse button, this event listener is triggered. 
// Inside the event listener function, it retrieves the selected text using 
// window.getSelection().toString(). 
// If there is any selected text, it calls the saveSelectedText() function 
// and passes the selected text as an argument.


document.addEventListener('mouseup', function(event) {
    var selectedText = window.getSelection().toString();
    if (selectedText !== '') {
        saveSelectedText(selectedText);
        createButton(); // Call the createButton() function
    }
});


// The saveSelectedText() function is called when there is selected text. 
// It performs an AJAX request to the server using the XMLHttpRequest object. 
// The request is a POST request to the root URL ('/'). 
// It sets the request header to specify that the content type is application/x-www-form-urlencoded. 
// When the response is received, the onload event handler is triggered. 
// It checks if the response status is 200 (indicating a successful response) and logs the response text 
// to the console using console.log(xhr.responseText). 
// The selected text is sent as data in the request body using the send() method. 
// It is appended to the URL-encoded string 'selected_text=' + encodeURIComponent(text). 
// The encodeURIComponent() function is used to properly encode the selected text to handle special characters. 
// Overall, this code sets up an event listener that captures the selected text on a webpage 
// and sends it to the server using an AJAX request when the user releases the mouse button. 
// The server can then process the selected text and perform any necessary actions.


// Function saveSelectedText(text):

// This function takes a parameter text as the selected text.
// It creates a new XMLHttpRequest object xhr to send an HTTP POST request to the root URL ('/').
// It sets the request header Content-Type to 'application/x-www-form-urlencoded' to specify the 
// type of data being sent.
// It defines an onload event handler for the XMLHttpRequest object, 
// which will be triggered when the response is received.
// Inside the onload event handler, it checks if the response status is 200 
// (indicating a successful response) using xhr.status === 200.
// If the response status is 200, it logs the response text to the console using 
// console.log(xhr.responseText).
// Finally, it sends the POST request with the selected text as the
// request body using xhr.send('selected_text=' + encodeURIComponent(text)).

// Specifications:
/* The Content-Type header with the value 'application/x-www-form-urlencoded' is used to specify the format of the data being sent in an HTTP request.

In the context of the code you provided, it is used when making a POST request with XMLHttpRequest to send data to the server. The 'application/x-www-form-urlencoded' format is a way of encoding form data to be included in the body of the request.

When this content type is set, the data is encoded in a format that follows the key=value pairs separated by the & symbol convention. This encoding is commonly used when submitting HTML forms.

For example, if you have a form with two fields, username and password, and the user inputs the values john and secretpassword, respectively, the encoded data would look like this: 'username=john&password=secretpassword'.

By setting the Content-Type to 'application/x-www-form-urlencoded', you indicate to the server that the data being sent in the request body is in this specific format. This allows the server to correctly parse and process the data on the server-side.

In summary, 'application/x-www-form-urlencoded' is a content type used to send form data in an HTTP request, where the data is encoded as key=value pairs separated by &. */

function saveSelectedText(text) {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log(xhr.responseText);
        }
    };
    xhr.send('selected_text=' + encodeURIComponent(text));
}


// Function createButton():

// This function creates a new button dynamically using document.createElement('button').
// It sets the text content of the button to 'New Button' using newButton.textContent = 'New Button'.
// It defines an onclick event handler for the button, which will be triggered when the button is clicked.
// Inside the onclick event handler, it calls a function from function.py 
// (replace function1 with the appropriate function name) to get the result.
// It displays an alert with the message 'New Button Result: ' concatenated with the result.
// Finally, it appends the new button to the <body> element of the document using document.body.appendChild(newButton).
// These two functions work together to capture the selected text, 
// send it to the server using an AJAX request, and dynamically create a new button. When the new button is clicked, it executes a function from function.py and displays the result in an alert.
function createButton() {
    var newButton = document.createElement('button');
    newButton.textContent = 'New Button';
    newButton.onclick = function() {
        // Call the function from function.py when the new button is clicked
        var result = function1(); // Replace function1 with the appropriate function name
        alert('New Button Result: ' + result);
    };
    document.body.appendChild(newButton);
}

