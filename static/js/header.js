let isSidebarOpen = false;

function ToggleSidebar() {
    isSidebarOpen = !isSidebarOpen;

    let sidebar = document.getElementById("header-sidebar");
    if (isSidebarOpen) {
        sidebar.style.transform = "scaleX(1)"
    } else {
        sidebar.style.transform = "scaleX(0)"
    }
}