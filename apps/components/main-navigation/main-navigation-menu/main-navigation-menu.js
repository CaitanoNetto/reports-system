document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("toggleMainNavMenuButton");
    const menu = document.getElementById("mainNavMenu");
    let expanded = true;
    btn.addEventListener("click", function () {
        expanded = !expanded;
        menu.classList.toggle("--is-opened", expanded);
        btn.classList.toggle("--is-expanded", expanded);

        const groupNames = document.querySelectorAll(".main-navigation-menu__groups__name");
        groupNames.forEach(function (el) {
            el.classList.toggle("--is-expanded", expanded);
        });
        const links = document.querySelectorAll(".main-navigation-menu__link");
        links.forEach(function (el) {
            el.classList.toggle("--is-expanded", expanded);
        });
    });
});

function onClickMenuItem() {
    const menu = document.getElementById("mainNavMenu");
    menu.classList.remove("--is-opened");
}
