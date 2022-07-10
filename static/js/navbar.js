//------------------- profile image dropdown------------------
function profFunction() {
    document.getElementById("profDrop").classList.toggle("show");
}
window.onclick = function (event) {
    if (!event.target.matches('.profimg')) {
        var dropdowns = document.getElementsByClassName("profdrop-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

//-------------------- responsive navbar----------------------
const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");

hamburger.addEventListener("click", () => {
    hamburger.classList.toggle("active");
    navMenu.classList.toggle("active");
})