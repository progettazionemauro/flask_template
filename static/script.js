// Executes when the document is fully loaded
document.addEventListener('DOMContentLoaded', function() {

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
  
    // Function to update the object list
    function updateObjectList() {
      // Creates a new XMLHttpRequest object
      var xhr = new XMLHttpRequest();
  
      // Defines the callback function to handle the AJAX response
      xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
            // Executes when the server responds with a successful message
            
            var responseHTML = document.createElement('html');
            responseHTML.innerHTML = xhr.responseText;
  
            // Updates the content of the 'object-list' element with the response data
            var objectList = responseHTML.querySelector('#object-list');
            document.getElementById('object-list').innerHTML = objectList.innerHTML;
          }
        }
      };
  
      // Sends a GET request to the specified URL
      xhr.open('GET', '/');
      xhr.send();
    }
  
    // Updates the object list when the page loads
    updateObjectList();
  
  });
  
