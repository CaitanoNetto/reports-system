document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("toggleMenuButton");
    const container = document.getElementById("navMenuContainer");
    let opened = false;
    btn.addEventListener("click", function () {
        opened = !opened;
        container.classList.toggle("--is-opened", opened);
    });
});
