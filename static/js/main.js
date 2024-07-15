
// GET SEARCH FORM AND PAGE LINKS
let searchForm = document.getElementById('searchForm')
let pageLinks = document.getElementsByClassName('page-link')

// ENSURE SEARCH FORM EXISTS
if(searchForm){
    for (let i=0; pageLinks.length > i; i++){
    pageLinks[i].addEventListener('click', function (e) {
        e.preventDefault()
        
        // GET THE DATA ATTRIBUTE
        let page = this.dataset.page
        
        // ADD HIDDEN SEARCH INPUT TO FORM
        searchForm.innerHTML += `<input value=${page} name="page" hidden/>`

        // SUBMIT FORM
        searchForm.submit()
    })
    }
}


// Rolling Sticky Bar
document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM fully loaded and parsed");
    
    window.onscroll = function() {
        console.log("Scroll event triggered");
        
        var stickyBar = document.getElementById("sticky-bar");
        var headerHeight = document.querySelector(".header").offsetHeight;
        console.log("Header height:", headerHeight);
        console.log("Page Y Offset:", window.pageYOffset);
        
        if (window.pageYOffset > headerHeight) {
            console.log("Adding sticky class");
            stickyBar.classList.add("sticky");
        } else {
            console.log("Removing sticky class");
            stickyBar.classList.remove("sticky");
        }
    };
});

// Preventing Double Click Dele
document.addEventListener("DOMContentLoaded", function() {
    const confirmationInput = document.getElementById("confirmationInput");
    const confirmButton = document.getElementById("confirmButton");

    confirmationInput.addEventListener("input", function() {
        if (confirmationInput.value.trim().toLowerCase() === "delete") {
            confirmButton.style.display = "inline-block";
        } else {
            confirmButton.style.display = "none";
        }
    });
});
