document.addEventListener("DOMContentLoaded", function () {
    const headerBtn = document.getElementById("toggleMenuButton");
    const navMenu = document.getElementById("mainNavMenu");
    let opened = false;
    headerBtn.addEventListener("click", function () {
        opened = !opened;
        if (navMenu) {
            navMenu.classList.toggle("--is-opened", opened);
        }
    });
});
