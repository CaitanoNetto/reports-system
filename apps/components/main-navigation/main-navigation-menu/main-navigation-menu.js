document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("toggleMainNavMenuButton");
    const menu = document.getElementById("mainNavMenu");
    let opened = false;
    btn.addEventListener("click", function () {
        opened = !opened;
        menu.classList.toggle("--is-opened", opened);
        btn.classList.toggle("--is-expanded", opened);
    });
});
