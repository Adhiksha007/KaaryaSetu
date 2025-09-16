document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.getElementById("toggleSidebar");
    const sidebar = document.getElementById("sidebarWrapper");

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener("click", () => {
            sidebar.classList.toggle("show");
        });
    }

    const sidebarLinks = document.querySelectorAll(".sidebar-link");
    const sections = document.querySelectorAll(".section-content");

    sidebarLinks.forEach(link => {
        link.addEventListener("click", () => {
            const targetId = link.getAttribute("data-target");

            sidebarLinks.forEach(l => l.classList.remove("active"));
            link.classList.add("active");

            sections.forEach(section => section.classList.remove("active"));

            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.classList.add("active");
            }

            if (window.innerWidth < 768) {
                sidebar.classList.remove("show");
            }
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

    window.addSection = function (X, Y) {
        const container = document.getElementById(X);
        const entries = container.querySelectorAll(Y);
        const lastEntry = entries[entries.length - 1];
        const inputs = lastEntry.querySelectorAll("input");
        let allFilled = true;

        inputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add("is-invalid");
                allFilled = false;
            } else {
                input.classList.remove("is-invalid");
            }
        });

        if (!allFilled) return;

        const clone = lastEntry.cloneNode(true);
        clone.querySelectorAll("input, textarea").forEach(input => {
            input.value = "";
            input.classList.remove("is-invalid");
        });
        container.appendChild(clone);
    }

    window.saveSection = function (sectionId) {
        const formData = new FormData();

        if (sectionId === 'profile') {
            formData.append('phone', document.getElementById('phone').value);
        }

        if (sectionId === 'preferences') {
            formData.append('titles', document.querySelector('#preferences input[placeholder*="Software"]').value);
            formData.append('locations', document.querySelector('#preferences input[placeholder*="Remote"]').value);
            formData.append('salary', document.querySelector('#preferences input[placeholder*="₹"]').value);
            formData.append('employment_type', document.querySelector('#preferences select').value);
            formData.append('relocate', document.querySelectorAll('#preferences select')[1].value);
        }

        if (sectionId === 'skills') {
            formData.append('skills', document.querySelector('[name="skills"]').value);
            formData.append('languages', document.querySelector('[name="languages"]').value);

            const otherDocsInput = document.querySelector('[name="certification[]"]');
            if (otherDocsInput && otherDocsInput.files.length > 0) {
                for (let i = 0; i < otherDocsInput.files.length; i++) {
                    formData.append('certification[]', otherDocsInput.files[i]);
                }
            }

            const educations = [];
            document.querySelectorAll('#education-section .education-entry').forEach(entry => {
                educations.push({
                    school: entry.querySelector('[name="school"]').value,
                    start_date: entry.querySelector('[name="start_date"]').value,
                    end_date: entry.querySelector('[name="end_date"]').value,
                    qualification: entry.querySelector('[name="qualification"]').value,
                    cgpa: entry.querySelector('[name="percentage"]').value,
                    city: entry.querySelector('[name="city"]').value,
                    state: entry.querySelector('[name="state"]').value,
                    country: entry.querySelector('[name="country"]').value
                });
            });
            formData.append('educations', JSON.stringify(educations));
        }

        if (sectionId === 'experience') {
            const experiences = [];
            document.querySelectorAll('#experience-section .experience-entry').forEach(entry => {
                experiences.push({
                    company: entry.querySelector('[name="company"]').value,
                    role: entry.querySelector('[name="role"]').value,
                    start_date: entry.querySelector('[name="start_date"]').value,
                    end_date: entry.querySelector('[name="end_date"]').value,
                    description: entry.querySelector('[name="description"]').value,
                    technologies: entry.querySelector('[name="technologies"]').value
                });
            });
            formData.append('experiences', JSON.stringify(experiences));
        }

        if (sectionId === 'documents') {
            const resumeInput = document.querySelector('[name="resume"]');
            if (resumeInput && resumeInput.files[0]) {
                formData.append('resume', resumeInput.files[0]);
            }

            const otherDocsInput = document.querySelector('[name="documents[]"]');
            if (otherDocsInput && otherDocsInput.files.length > 0) {
                for (let i = 0; i < otherDocsInput.files.length; i++) {
                    formData.append('documents[]', otherDocsInput.files[i]);
                }
            }
        }

        if (sectionId === 'notifications') {
            const frequency = document.querySelector('#notifications select').value;
            formData.append('notification_frequency', frequency);
        }

        fetch(`/dashboard/save/${sectionId}`, {
            method: 'POST',
            body: formData,
        })
        .then(res => res.json())
        .then(data => alert(data.message || 'Saved successfully!'))
        .catch(err => {
            alert('Failed to save changes.');
            console.error(err);
        });
    }

    const updateBtn = document.querySelector('.btn-warning');
    if (updateBtn) {
        updateBtn.addEventListener('click', async () => {
            const currentPassword = document.getElementById('currentPassword').value.trim();
            const newPassword = document.getElementById('newPassword').value.trim();
            const confirmPassword = document.getElementById('confirmPassword').value.trim();

            const formData = new FormData();
            formData.append('currentPassword', currentPassword);
            formData.append('newPassword', newPassword);
            formData.append('confirmPassword', confirmPassword);

            const res = await fetch('/update-password', {
                method: 'POST',
                body: formData
            });

            const data = await res.json();
            alert(data.message);
        });
    }

    const deleteBtn = document.querySelector('.deleteAccount');
    if (deleteBtn) {
        deleteBtn.addEventListener('click', async () => {
            if (!confirm('Are you sure you want to delete your account? This action cannot be undone.')) return;

            const res = await fetch('/delete-account', { method: 'POST' });
            const data = await res.json();
            alert(data.message);

            if (res.ok) {
                window.location.href = '/';
            }
        });
    }

    const manage2FABtn = document.querySelector('.btn-secondary');
    if (manage2FABtn) {
        manage2FABtn.addEventListener('click', () => {
            alert('2FA management is not implemented yet.');
        });
    }
});
