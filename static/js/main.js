document.addEventListener('DOMContentLoaded', () => {

    // Handle modal opening (if modal ID is globally passed)
    if (window.openModalId) {
        const modalMap = {
            loginModal: "openLoginModalBtn",
            registerModal: "openRegisterModalBtn",
            forgotPasswordModal: "openForgotModalBtn",
            resetPasswordModal: "openResetModalBtn"
        };

        const triggerId = modalMap[window.openModalId];
        if (triggerId) {
            const btn = document.getElementById(triggerId);
            if (btn) btn.click();
            else console.warn("Trigger button not found for modal:", window.openModalId);
        } else {
            console.warn("Unknown modal ID:", window.openModalId);
        }
    }

    // Password match validation in Register modal
    const registerForm = document.querySelector('#registerModal form');
    if (registerForm) {
        registerForm.addEventListener('submit', function (e) {
            const pwd = document.getElementById('reg_password');
            const confirm = document.getElementById('confirm_password');
            if (pwd.value !== confirm.value) {
                confirm.setCustomValidity("Passwords do not match");
                confirm.reportValidity();
                e.preventDefault();
            } else {
                confirm.setCustomValidity("");
            }
        });
    }

    const toggleBtn = document.getElementById("toggleSidebar");
    const sidebar = document.getElementById("navbarContent");

    // Toggle sidebar on button click
    toggleBtn.addEventListener("click", () => {
      sidebar.classList.toggle("show");
    });

    // Auto-close sidebar when any link inside is clicked
    sidebar.querySelectorAll("a.nav-link").forEach(link => {
      link.addEventListener("click", () => {
        sidebar.classList.remove("show");
      });
    });

    // Auto-close sidebar when clicking outside of it
    document.addEventListener("click", (event) => {
      const isClickInsideSidebar = sidebar.contains(event.target);
      const isToggleButton = toggleBtn.contains(event.target);

      // Close if clicked outside sidebar and not on toggle
      if (!isClickInsideSidebar && !isToggleButton) {
        sidebar.classList.remove("show");
      }
    });


    const themeToggle = document.querySelector(".theme");
    const dayNight = document.querySelector(".day-night");
    const icon = dayNight.querySelector("i");

    // Apply saved theme
    const savedTheme = localStorage.getItem("theme") || "light";
    document.body.classList.toggle("dark", savedTheme === "dark");
    icon.classList.add(savedTheme === "dark" ? "fa-sun" : "fa-moon");

    // Toggle theme on click
    themeToggle.addEventListener("click", () => {
        const isDark = document.body.classList.toggle("dark");
        localStorage.setItem("theme", isDark ? "dark" : "light");

        icon.classList.toggle("fa-sun", isDark);
        icon.classList.toggle("fa-moon", !isDark);
    });
});

