document.addEventListener("DOMContentLoaded", () => {
    const savedTheme = localStorage.getItem("theme") || "light";
    document.body.classList.toggle("dark", savedTheme === "dark");
});
