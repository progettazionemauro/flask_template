document.addEventListener('DOMContentLoaded', function() {
    // Create button click event listener
    document.getElementById('object-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevents the default form submission behavior

        // Retrieves the value entered in the name input field
        var name = document.getElementById('name-input').value;

        // Create a new FormData object to send the text data
        var formData = new FormData();
        formData.append('name', name);

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
                    location.reload(); // Refreshes the page
                }
            }
        };

        // Sends a POST request to the specified URL with the form data
        xhr.open('POST', '/add');
        xhr.send(formData);
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

    // Socket event listeners
    var socket = io(); // Connect to the SocketIO server

    // Handle 'object_created' event
    socket.on('object_created', function(data) {
        // Update the UI with the newly created object
        var newRow = document.createElement('tr');
        newRow.innerHTML = '<td>' + data.name + '</td><td>' +
            '<div class="d-flex align-items-center">' +
            '<input type="text" class="update-input form-control me-2" data-id="' + data.id + '" placeholder="Update text">' +
            '<button class="update-btn btn btn-primary me-2" data-id="' + data.id + '">Update</button>' +
            '<button class="delete-btn btn btn-danger" data-id="' + data.id + '">Delete</button>' +
            '<button class="upload-btn btn btn-success" data-id="' + data.id + '">Upload File</button>' +
            '<input type="file" class="form-control-file file-input" data-id="' + data.id + '" name="file">' +
            '</div></td>';
        document.getElementById('object-list').appendChild(newRow);

        // Refresh the object list
        updateObjectList();
    });

    // Handle 'object_updated' event
    socket.on('object_updated', function(data) {
        // Update the UI with the updated object
        var inputField = document.querySelector('input[data-id="' + data.id + '"]');
        inputField.value = data.name;

        // Refresh the object list
        updateObjectList();
    });

    // Handle 'object_deleted' event
    socket.on('object_deleted', function(data) {
        // Remove the deleted object from the UI
        var objectRow = document.querySelector('tr[data-id="' + data.id + '"]');
        if (objectRow) {
            objectRow.remove();
        }

        // Refresh the object list
        updateObjectList();
    });

    // Upload button click event listener
    document.addEventListener('click', function(event) {
        var target = event.target;
        if (target.classList.contains('upload-btn')) {
            var objectId = target.getAttribute('data-id');
            var fileInput = document.querySelector('input.file-input[data-id="' + objectId + '"]');
            var file = fileInput.files[0]; // Assuming single file upload

            // Create a new FormData object to send the file data
            var formData = new FormData();
            formData.append('file', file);

            // Creates a new XMLHttpRequest object
            var xhr = new XMLHttpRequest();

            // Defines the callback function to handle the AJAX response
            xhr.onreadystatechange = function() {
                if (xhr.readyState === XMLHttpRequest.DONE) {
                    if (xhr.status === 200) {
                        // Handle the success response
                        alert(xhr.responseText); // Displays an alert with the response message
                        updateObjectList(); // Updates the object list
                        location.reload(); // Refresh the page
                    }
                }
            };

            // Sends a POST request to the specified URL with the form data
            xhr.open('POST', '/upload/' + objectId);
            xhr.send(formData);
        }
    });
});
