function toggleDropdown() {
    document.getElementById("dropdown-content").classList.toggle("show");
}

function selectOption(option) {
    document.getElementById("dropdown-label").children[0].textContent = option;
    document.getElementById("dropdown-content").classList.remove("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.custom-dropdown-label') && !event.target.matches('.custom-dropdown-label *')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        for (var i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

