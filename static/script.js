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
