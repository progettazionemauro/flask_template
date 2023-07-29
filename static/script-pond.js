// script-pond.js
document.addEventListener('DOMContentLoaded', function() {
    // Get the file input element with the 'filepond' class
    var fileInput = document.querySelector('.filepond');

    // Check if the FilePond library is loaded
    if (typeof FilePond !== 'undefined') {
        // Import the Image Preview plugin dynamically (no import needed for CDN)
        FilePond.registerPlugin(FilePondPluginImagePreview);

        // Create the FilePond instance for the file input element
        var pond = FilePond.create(fileInput);

        // Get the links with the file-preview-link class
        var filePreviewLinks = document.querySelectorAll('.file-preview-link');

        // Add click event listener to each file preview link
        filePreviewLinks.forEach(function(link) {
            link.addEventListener('click', function(event) {
                event.preventDefault();
                var objectId = link.getAttribute('data-id');

                // Get the FilePond file item for the corresponding object ID
                var fileItem = pond.getFile(function(file) {
                    return file.id === objectId;
                });

                // Open the file preview for the selected file
                pond.open(fileItem);
            });
        });
    } else {
        console.error('FilePond library not loaded. Make sure you have included the FilePond script.');
    }
});
