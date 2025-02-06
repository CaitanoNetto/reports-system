document.addEventListener("DOMContentLoaded", function () {
    const menuToggleButton = document.getElementById("toggleMenuButton");
    const navMenu = document.querySelector(".main-navigation-menu");
    const contentOutlet = document.querySelector(".main-navigation__content__outlet");

    function toggleMenu() {
        navMenu.classList.toggle("hidden");
        contentOutlet.classList.toggle("menu-opened");
    }

    if (menuToggleButton) {
        menuToggleButton.addEventListener("click", toggleMenu);
    }
});
