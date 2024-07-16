
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
    
    window.onscroll = function() {
        var stickyBar = document.getElementById("sticky-bar");
        var headerHeight = document.querySelector(".header").offsetHeight;

        
        if (window.pageYOffset > headerHeight) {
            stickyBar.classList.add("sticky");
        } else {
            stickyBar.classList.remove("sticky");
        }
    };
});
