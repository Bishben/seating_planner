document.addEventListener("DOMContentLoaded", function () {
  // THEME TOGGLE
  if (localStorage.getItem("theme") === "light") {
      document.body.classList.remove("dark-mode");
      document.body.classList.add("light-mode");
      document.getElementById("themeToggle").innerText = "☀️";
  }

  document.getElementById("themeToggle").addEventListener("click", function () {
      if (document.body.classList.contains("dark-mode")) {
          document.body.classList.remove("dark-mode");
          document.body.classList.add("light-mode");
          localStorage.setItem("theme", "light");
          this.innerText = "☀️";
      } else {
          document.body.classList.remove("light-mode");
          document.body.classList.add("dark-mode");
          localStorage.setItem("theme", "dark");
          this.innerText = "🌙";
      }
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
});