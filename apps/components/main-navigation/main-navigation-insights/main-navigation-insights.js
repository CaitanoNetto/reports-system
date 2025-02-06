document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("toggleInsightsButton");
    const sidebar = document.getElementById("insightsSidebar");
    let expanded = true;
    btn.addEventListener("click", function () {
        expanded = !expanded;
        sidebar.classList.toggle("--is-expanded", expanded);
        btn.classList.toggle("--is-expanded", expanded);
    });
});
