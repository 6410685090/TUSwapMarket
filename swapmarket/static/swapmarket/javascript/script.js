// script.js
document.addEventListener("DOMContentLoaded", function () {
    checkWindowSize();

    window.addEventListener("resize", function () {
        checkWindowSize();
    });

    function checkWindowSize() {
        const windowWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;

        const container = document.querySelector(".container");

        if (windowWidth < 600) {
            container.classList.add("responsive-layout");
        } else {
            container.classList.remove("responsive-layout");
        }
    }
});
