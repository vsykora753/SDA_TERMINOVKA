document.addEventListener("DOMContentLoaded", function() {
    const dropdowns = document.querySelectorAll(".dropdown"); // Vybere všechny dropdowny

    dropdowns.forEach(dropdown => {
        const submenu = dropdown.querySelector(".link_submenu");
        const arrow = dropdown.querySelector(".arrow");

        dropdown.addEventListener("mouseover", function() {
            submenu.style.display = "block";
        });

        dropdown.addEventListener("mouseout", function() {
            submenu.style.display = "none";
        });
    });
});
