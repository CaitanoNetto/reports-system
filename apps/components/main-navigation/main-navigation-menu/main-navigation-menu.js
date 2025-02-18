document.addEventListener("DOMContentLoaded", function () {
    const groups = [
        {
            name: 'Gerencial',
            modules: [
                { path: '', icon: 'home', label: 'Home' },
                { path: 'daily', icon: 'today', label: 'Acompanhamento Diário' }
            ]
        },
        {
            name: 'Default',
            modules: [
                { path: 'default', icon: 'report', label: 'Report Default' }
            ]
        }
    ];

    let collapsed = true; // Se `menu-collapsed` está no HTML, começamos como `true`.

    function renderMenu() {
        const container = document.getElementById("menuContainer");
        if (!container) return;
        container.innerHTML = "";

        const ulGroups = document.createElement("ul");
        ulGroups.classList.add("main-navigation-menu__groups");

        groups.forEach((group) => {
            const liGroup = document.createElement("li");
            const h4 = document.createElement("h4");
            h4.classList.add("main-navigation-menu__groups__name");
            h4.setAttribute("id", "menu-group-name");
            if (collapsed) {
                h4.classList.add("is-expanded");
            }
            h4.textContent = group.name;
            liGroup.appendChild(h4);

            const ulModules = document.createElement("ul");
            ulModules.classList.add("main-navigation-menu__modules");
            
            group.modules.forEach((module) => {
                const currentPathName = window.location.pathname.replace(/\//g, "")
                const modulePathName = module.path.replace(/\//g, "")
                
                const liModule = document.createElement("li");
                liModule.classList.add("main-navigation-menu__item");

                const a = document.createElement("a");
                a.classList.add("main-navigation-menu__link");
                a.setAttribute("id", "menu-navigation-link")
                if (collapsed) {
                    a.classList.add("is-expanded");
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
                if( currentPathName === modulePathName){
                    divIcon.classList.add("active_link_icon");
                }

                const divLabel = document.createElement("div");
                divLabel.classList.add("main-navigation-menu__link__label");
                divLabel.setAttribute("id", "menu-link-label");
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
        collapsed = !collapsed;
        renderMenu();
        
        const toggleBtn = document.getElementById("menuToggleBtn");
        if (toggleBtn) {
            toggleBtn.classList.toggle("is-expanded", collapsed);
            toggleBtn.querySelector(".icon").textContent = collapsed
            ? "keyboard_double_arrow_left"
            : "keyboard_double_arrow_right";
        }
        
        const menu = document.getElementById("mainNavMenu");
        const labels = document.querySelectorAll("#menu-link-label")
        const menuGroupNames = document.querySelectorAll("#menu-group-name")
        const menuNavigationLinks = document.querySelectorAll("#menu-navigation-link")
        
        if(!collapsed &&  labels) labels.forEach((label) => label.classList.toggle("hide-label"))
        if(!collapsed && menuGroupNames) menuGroupNames.forEach((menuGroupName) => menuGroupName.classList.toggle("hide-menu-group-name"))
        if(!collapsed && menuNavigationLinks) menuNavigationLinks.forEach((menuNavigationLink) => menuNavigationLink.classList.toggle("hide-menu-navigation-link"))
        if(menu) menu.classList.toggle("menu-collapsed");
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
