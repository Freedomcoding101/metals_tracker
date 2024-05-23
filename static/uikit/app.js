// Invoke Functions Call on Document Loaded
document.addEventListener('DOMContentLoaded', function () {
hljs.highlightAll();

});
document.addEventListener('DOMContentLoaded', function () {
    // Find all close buttons
    var closeButtons = document.querySelectorAll('.alert__close');
    
    // Loop through each close button
    closeButtons.forEach(function(closeButton) {
        // Add click event listener to each close button
        closeButton.addEventListener('click', function() {
            // Find the closest alert box to the clicked button
            var alertBox = closeButton.closest('.alert');
            if (alertBox) {
                // Hide the alert box
                alertBox.style.display = 'none';
            }
        });
    });
});

function goBack() {
    window.history.back();
}
