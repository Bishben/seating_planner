document.addEventListener("DOMContentLoaded", () => {

  // 1. THEME TOGGLE FUNCTIONALITY

  // Define the function to set dark mode
  function setDarkMode() {
    // Remove light mode classes and add dark mode classes
    document.body.classList.remove("light-mode");
    document.body.classList.add("dark-mode");
    document.getElementById("themeToggle").innerText = "🌙";

    // Apply Dark theme to all cards
    const cards = document.querySelectorAll(".card");
    cards.forEach((card) => {
      card.classList.remove("text-bg-light");
      card.classList.add("text-bg-dark", "dark-border");
    });

    // Apply Dark Theme to all Card Lists (if they exist)\
    const lists = document.querySelectorAll(".list-group-item");
    lists.forEach((list) => {
      list.classList.remove("text-bg-light");
      list.classList.add("text-bg-dark");
    });

    localStorage.setItem("theme", "dark");
  }

  // Define the function to set light mode
  function setLightMode() {
    // Remove dark mode classes and add light mode classes
    document.body.classList.remove("dark-mode");
    document.body.classList.add("light-mode");
    document.getElementById("themeToggle").innerText = "☀️";

    // Apply Light theme to all cards
    const cards = document.querySelectorAll(".card");
    cards.forEach((card) => {
      card.classList.remove("text-bg-dark", "dark-border");
      card.classList.add("text-bg-light");
    });

    // Apply Light Theme to all Card Lists (if they exist)
    const lists = document.querySelectorAll(".list-group-item");
    lists.forEach((list) => {
      list.classList.remove("text-bg-dark", "dark-border");
      list.classList.add("text-bg-light");
    });

    localStorage.setItem("theme", "light");
  }

  // Check the current theme from localStorage and set the initial theme
  const currentTheme = localStorage.getItem("theme");
  if(currentTheme === "dark") {
    setDarkMode();
  } else if (currentTheme === "light") {
    setLightMode();
  } else {
    // Default to light mode if no theme is set in localStorage
    setLightMode();
  }

  // Add event listener to the theme toggle button
  document.getElementById("themeToggle").addEventListener("click", () => {
    // Toggle between light and dark mode
    if (document.body.classList.contains("dark-mode")) {
      setLightMode();
    } 
    else {
      setDarkMode();
    }
  });
});

// DROPDOWN MENU FUNCTIONALITY
const dropdownMenu = document.getElementById("dropdownMenu");
const dropdownItems = document.querySelectorAll(".dropdown-option");

// Load previously selected item from localStorage
let selectedItem = localStorage.getItem("selectedDropdownItem");
let selectedHref = localStorage.getItem("selectedDropdownHref");

if (selectedItem && selectedHref) {
  dropdownMenu.textContent = selectedItem;
  dropdownMenu.setAttribute("href", selectedHref);
}

dropdownItems.forEach((item) => {
  item.addEventListener("click", function (event) {
    event.preventDefault(); // Prevent default navigation

    let selectedText = this.textContent;
    let selectedHref = this.getAttribute("href");

    // Store the selected item in localStorage
    localStorage.setItem("selectedDropdownItem", selectedText);
    localStorage.setItem("selectedDropdownHref", selectedHref);

    // Update the dropdown menu text
    dropdownMenu.textContent = selectedText;
    dropdownMenu.setAttribute("href", selectedHref);

    // Navigate to the new page
    window.location.href = selectedHref;
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const searchForm = document.getElementById("searchForm");
  const searchInput = document.getElementById("searchInput");

  if (!searchForm || !searchInput) {
    console.error("Unable To Find SEARCH FORM");
    return;
  }

  // Get current path
  const currentPath = window.location.pathname;
  console.log(currentPath);

  if (currentPath.includes("events")) {
    searchInput.placeholder = "Search Events...";
  } else if (currentPath.includes("history")) {
    searchInput.placeholder = "Search History...";
  } else if (currentPath.includes("subjects")) {
    searchInput.placeholder = "Search Subjects...";
  } else if (currentPath.includes("branches")) {
    searchInput.placeholder = "Search Branches...";
  } else if (currentPath.includes("rooms")) {
    searchInput.placeholder = "Search Rooms...";
  }
});
