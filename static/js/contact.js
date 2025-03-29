document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    form.addEventListener("submit", function (event) {
        event.preventDefault();
        setTimeout(() => {
            form.reset();
            alert("Your message was sent successfully!");
        }, 500);
    });
});