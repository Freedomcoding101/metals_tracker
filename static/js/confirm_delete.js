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
