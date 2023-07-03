document.addEventListener('DOMContentLoaded', function() {
    // Executes when the DOM content has finished loading

    // Attaches a submit event listener to the form with ID 'object-form'
    document.getElementById('object-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevents the default form submission behavior

        // Retrieves the value entered in the name input field
        var name = document.getElementById('name-input').value;

        // Creates a new XMLHttpRequest object
        var xhr = new XMLHttpRequest();

        // Defines the callback function to handle the AJAX response
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // Executes when the server responds with a successful message
                    alert(xhr.responseText); // Displays an alert with the response message
                    document.getElementById('name-input').value = ''; // Clears the name input field
                    updateObjectList(); // Updates the object list
                    setTimeout(function() {
                        location.reload(); // Refreshes the page after a delay (2 seconds)
                    }, 2000);
                }
            }
        };

        // Sends a POST request to the specified URL with the name as data
        xhr.open('POST', '/add');
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.send('name=' + encodeURIComponent(name));
    });

    // Update button click event listener
    document.addEventListener('click', function(event) {
        var target = event.target;
        if (target.classList.contains('update-btn')) {
            var objectId = target.getAttribute('data-id');
            var inputField = document.querySelector('input[data-id="' + objectId + '"]');
            var updatedText = inputField.value; // Retrieve the value from the input field

            // Send an AJAX request to the '/update' route with the updated data
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        // Handle the success response
                        updateObjectList(); // Update the object list
                        location.reload(); // Refresh the page
                    }
                }
            };
            xhr.open('POST', '/update/' + objectId);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.send(JSON.stringify({ name: updatedText })); // Send the updated text as JSON data with the 'name' key
        }
    });

    // Delete button click event listener
    document.addEventListener('click', function(event) {
        var target = event.target;
        if (target.classList.contains('delete-btn')) {
            var objectId = target.getAttribute('data-id');

            // Send an AJAX request to the '/delete' route to delete the object
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        // Handle the success response
                        updateObjectList(); // Update the object list
                        location.reload(); // Refresh the page
                    }
                }
            };
            xhr.open('POST', '/delete/' + objectId);
            xhr.send();
        }
    });

    // Function to refresh the object list
    function updateObjectList() {
        // Retrieve the updated object list from the server using AJAX
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    // Handle the success response
                    var responseHTML = document.createElement('html');
                    responseHTML.innerHTML = xhr.responseText;

                    // Updates the content of the 'object-list' element with the response data
                    var objectList = responseHTML.querySelector('#object-list');
                    document.getElementById('object-list').innerHTML = objectList.innerHTML;
                }
            }
        };
        xhr.open('GET', '/');
        xhr.send();
    }

    // Updates the object list when the page loads
    updateObjectList();
});
