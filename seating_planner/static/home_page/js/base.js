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

  const dropdownMenu = document.getElementById("dropdownMenu");
    const dropdownItems = document.querySelectorAll(".dropdown-option");

    dropdownItems.forEach(item => {
        item.addEventListener("click", function (event) {
            event.preventDefault(); // Prevent default navigation
            
            let selectedText = this.textContent;
            let selectedHref = this.getAttribute("href");

            // Get the original button text (Exams) and link
            let originalText = dropdownMenu.textContent.trim();
            let originalHref = dropdownMenu.getAttribute("href");

            // Swap the button text with the selected option's text
            dropdownMenu.textContent = selectedText;
            dropdownMenu.setAttribute("href", selectedHref);

            // Update the clicked item to the original button text
            this.textContent = originalText;
            this.setAttribute("href", originalHref);
        });
    });
});