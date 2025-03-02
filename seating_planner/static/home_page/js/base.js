document.addEventListener("DOMContentLoaded", () => {
    // THEME TOGGLE
    if (localStorage.getItem("theme") === "light") {
      document.body.classList.remove("dark-mode");
      document.body.classList.add("light-mode");
      document.getElementById("themeToggle").innerText = "☀️";
      
      // Apply light theme to all cards
      const cards = document.querySelectorAll(".card");
      cards.forEach(card => {
        card.classList.remove("text-bg-dark");
        card.classList.add("text-bg-light");
      });
    }
  
    document.getElementById("themeToggle").addEventListener("click", () => {
      const cards = document.querySelectorAll(".card");
  
      if (document.body.classList.contains("dark-mode")) {
        document.body.classList.remove("dark-mode");
        document.body.classList.add("light-mode");
        localStorage.setItem("theme", "light");
        document.getElementById("themeToggle").innerText = "☀️";
        
        // Apply light theme to all cards
        cards.forEach(card => {
          card.classList.remove("text-bg-dark");
          card.classList.add("text-bg-light");
        });
      } else {
        document.body.classList.remove("light-mode");
        document.body.classList.add("dark-mode");
        localStorage.setItem("theme", "dark");
        document.getElementById("themeToggle").innerText = "🌙";
        
        // Apply dark theme to all cards
        cards.forEach(card => {
          card.classList.remove("text-bg-light");
          card.classList.add("text-bg-dark");
        });
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

  dropdownItems.forEach(item => {
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

document.addEventListener("DOMContentLoaded", ()=> {
    const searchForm = document.getElementById("searchForm");
    const searchInput = document.getElementById("searchInput");

    // Get current path
    const currentPath = window.location.pathname;

    if (currentPath.includes("events")) {
        searchForm.action = "{% url 'home_page:events' %}";
        searchInput.placeholder = "Search Events...";
    } else if (currentPath.includes("history")) {
        searchForm.action = "{% url 'home_page:history' %}";
        searchInput.placeholder = "Search History...";
    } else if (currentPath.includes("subjects")) {
        searchForm.action = "{% url 'home_page:subjects' %}";
        searchInput.placeholder = "Search Subjects...";
    } else if (currentPath.includes("branches")) {
        searchForm.action = "{% url 'home_page:branches' %}";
        searchInput.placeholder = "Search Branches...";
    } else if (currentPath.includes("rooms")) {
        searchForm.action = "{% url 'home_page:rooms' %}";
        searchInput.placeholder = "Search Rooms...";
    }
});