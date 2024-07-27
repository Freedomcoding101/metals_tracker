document.addEventListener("DOMContentLoaded", function() {
    // GET SEARCH FORM AND PAGE LINKS
    let searchForm = document.getElementById('searchForm');
    let pageLinks = document.getElementsByClassName('page-link');

    // ENSURE SEARCH FORM EXISTS
    if (searchForm) {
        for (let i = 0; pageLinks.length > i; i++) {
            pageLinks[i].addEventListener('click', function(e) {
                e.preventDefault();

                // GET THE DATA ATTRIBUTE
                let page = this.dataset.page;

                // ADD HIDDEN SEARCH INPUT TO FORM
                searchForm.innerHTML += `<input value=${page} name="page" hidden/>`;

                // SUBMIT FORM
                searchForm.submit();
            });
        }
    }

    // Rolling Sticky Bar
    window.onscroll = function() {
        var stickyBar = document.getElementById("sticky-bar");
        var headerHeight = document.querySelector(".header").offsetHeight;

        if (window.pageYOffset > headerHeight) {
            stickyBar.classList.add("sticky");
        } else {
            stickyBar.classList.remove("sticky");
        }
    };

    // Cancel Doubleclicks on delete button and change text to Deleting...
    function handleDelete() {
        console.log("handleDelete function called");
        var deleteButton = document.getElementById('delete-button');
        deleteButton.disabled = true; // Disable the button to prevent double-clicks

        // Optionally, you can change the button text to indicate the action is in progress
        deleteButton.innerText = 'Deleting...';

        // Submit the form or make an AJAX request to delete the item
        // For example, if you are using a form:
        document.getElementById('delete-form').submit();

        // If you are using AJAX, make the request here and re-enable the button if the request fails
    }

    // Bind the handleDelete function to the delete button
    var deleteButton = document.getElementById('delete-button');
    if (deleteButton) {
        deleteButton.addEventListener('click', handleDelete);
    }
});