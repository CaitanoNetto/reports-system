document.addEventListener("DOMContentLoaded", function () {
    const groups = [
        {
            name: 'Gerencial',
            modules: [
                { path: '', icon: 'home', label: 'Home' },
                { path: 'daily/', icon: 'today', label: 'Acompanhamento Diário' }
            ]
        },
        {
            name: 'Default',
            modules: [
                { path: 'default/', icon: 'report', label: 'Report Default' }
            ]
        }
    ];

    let expanded = true; // Se `menu-opened` está no HTML, começamos como `true`.

    function renderMenu() {
        const container = document.getElementById("menuContainer");
        if (!container) return;
        container.innerHTML = '';

        const ulGroups = document.createElement("ul");
        ulGroups.classList.add("main-navigation-menu__groups");

        groups.forEach(group => {
            const liGroup = document.createElement("li");
            const h4 = document.createElement("h4");
            h4.classList.add("main-navigation-menu__groups__name");
            if (expanded) {
                h4.classList.add("--is-expanded");
            }
            h4.textContent = group.name;
            liGroup.appendChild(h4);

            const ulModules = document.createElement("ul");
            ulModules.classList.add("main-navigation-menu__modules");

            group.modules.forEach(module => {
                const liModule = document.createElement("li");
                liModule.classList.add("main-navigation-menu__item");

                const a = document.createElement("a");
                a.classList.add("main-navigation-menu__link");
                if (expanded) {
                    a.classList.add("--is-expanded");
                }
                a.href = `/${module.path}`;
                a.addEventListener("click", function () {
                    onClickMenuItem();
                });

                const divIcon = document.createElement("div");
                divIcon.classList.add("main-navigation-menu__link__icon");
                const spanIcon = document.createElement("span");
                spanIcon.classList.add("icon");
                spanIcon.textContent = module.icon;
                divIcon.appendChild(spanIcon);

                const divLabel = document.createElement("div");
                divLabel.classList.add("main-navigation-menu__link__label");
                const spanLabel = document.createElement("span");
                spanLabel.textContent = module.label;
                divLabel.appendChild(spanLabel);

                a.appendChild(divIcon);
                a.appendChild(divLabel);
                liModule.appendChild(a);
                ulModules.appendChild(liModule);
            });

            liGroup.appendChild(ulModules);
            ulGroups.appendChild(liGroup);
        });

        container.appendChild(ulGroups);
    }

    function toggleMenuExpansion() {
        expanded = !expanded;
        renderMenu();

        const toggleBtn = document.getElementById("menuToggleBtn");
        if (toggleBtn) {
            toggleBtn.classList.toggle("--is-expanded", expanded);
            toggleBtn.querySelector(".icon").textContent = expanded
                ? "keyboard_double_arrow_left"
                : "keyboard_double_arrow_right";
        }

        const menu = document.getElementById("mainNavMenu");
        if (menu) {
            menu.classList.toggle("menu-opened", expanded);
        }
    }

    function onClickMenuItem() {
    }

    const toggleBtn = document.getElementById("menuToggleBtn");
    if (toggleBtn) {
        toggleBtn.addEventListener("click", toggleMenuExpansion);
    }

    window.toggleMenuExpansion = toggleMenuExpansion;
    window.onClickMenuItem = onClickMenuItem;

    renderMenu();
});