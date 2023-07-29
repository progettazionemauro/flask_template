// Function to handle the FilePond form submission
function handleFilePondFormSubmit() {
    // Retrieve the value entered in the name input field
    const name = document.getElementById('name-input').value;

    // Get the FilePond files
    const files = pond.getFiles();

    // Create a new FormData object to send the form data including the files
    const formData = new FormData();
    formData.append('name', name);

    // Append each FilePond file to the FormData object
    files.forEach(file => {
        formData.append('filepond', file.file);
    });

    // Create a new XMLHttpRequest object
    const xhr = new XMLHttpRequest();

    // Define the callback function to handle the AJAX response
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                // Executes when the server responds with a successful message
                alert(xhr.responseText); // Displays an alert with the response message
                document.getElementById('name-input').value = ''; // Clears the name input field
                pond.removeFiles(); // Clears the FilePond files
                updateObjectList(); // Updates the object list
            }
        }
    };

    // Sends a POST request to the specified URL with the form data
    xhr.open('POST', '/add');
    xhr.send(formData);
}

// Initialize FilePond on the file input element
FilePond.registerPlugin(FilePondPluginImagePreview);
const inputElement = document.querySelector('.filepond');
const pond = FilePond.create(inputElement);
