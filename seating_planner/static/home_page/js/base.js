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
