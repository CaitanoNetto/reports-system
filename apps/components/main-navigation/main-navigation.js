document.addEventListener("DOMContentLoaded", function () {
    const menuToggleButton = document.getElementById("toggleMenuButton");
    const navMenu = document.getElementById("mainNavMenu");

    function toggleMenu() {
        navMenu.classList.toggle("hidden");
    }

    if (menuToggleButton) {
        menuToggleButton.addEventListener("click", toggleMenu);
    }
});