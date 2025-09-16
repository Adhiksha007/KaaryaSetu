document.addEventListener('DOMContentLoaded', function () {
  const jobDetailsModal = document.getElementById('jobDetailsModal');
  if (!jobDetailsModal) return;

  jobDetailsModal.addEventListener('show.bs.modal', function (event) {
    const btn = event.relatedTarget;
    if (!btn) return;

    function set(id, value) {
      const el = document.getElementById(id);
      if (el) el.textContent = value || 'N/A';
    }

    set("modalTitle", btn.getAttribute("data-title"));
    set("modalCompany", btn.getAttribute("data-company"));
    set("modalWorkType", btn.getAttribute("data-worktype"));
    set("modalRole", btn.getAttribute("data-role"));
    set("modalExperience", btn.getAttribute("data-experience"));
    set("modalQualifications", btn.getAttribute("data-qualifications"));
    set("modalSkills", btn.getAttribute("data-skills"));
    set("modalResponsibilities", btn.getAttribute("data-responsibilities"));
    set("modalSalary", btn.getAttribute("data-salary"));
    set("modalBenefits", btn.getAttribute("data-benefits"));
    set("modalDescription", btn.getAttribute("data-description"));

    set("modalLocation", btn.getAttribute("data-location"));
    set("modalCity", btn.getAttribute("data-city"));
    set("modalState", btn.getAttribute("data-state"));
    set("modalZip", btn.getAttribute("data-zip"));
    set("modalCountry", btn.getAttribute("data-country"));
    set("modalLatitude", btn.getAttribute("data-lat"));
    set("modalLongitude", btn.getAttribute("data-lng"));
    set("modalSector", btn.getAttribute("data-sector"));
    set("modalIndustry", btn.getAttribute("data-industry"));
    set("modalCompanySize", btn.getAttribute("data-size"));
    set("modalCeo", btn.getAttribute("data-ceo"));
    set("modalTicker", btn.getAttribute("data-ticker"));
    set("modalPosted", btn.getAttribute("data-posted"));
    set("modalPreference", btn.getAttribute("data-preference"));
    set("modalContactPerson", btn.getAttribute("data-contact-person"));
    set("modalContact", btn.getAttribute("data-contact"));

    const applyButton = document.getElementById('applyButton');
    const websiteLink = document.getElementById('modalWebsite');

    if (applyButton) applyButton.href = btn.getAttribute('data-apply') || '#';
    if (websiteLink) websiteLink.href = btn.getAttribute('data-website') || '#';
  });

// document.getElementById('saveJobButton').setAttribute('data-job-id', btn.getAttribute("data-jobId"));  // jobId is the current job's ID

document.getElementById('saveJobButton').addEventListener('click', function (e) {
    e.preventDefault();
    const btn = e.relatedTarget;
    if (!btn) return;
    
    const jobId = btn.getAttribute("data-jobId");

    fetch('/save_job', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ job_id: jobId })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        alert('Job saved successfully!');
      } else {
        alert('Job already saved or an error occurred.');
      }
    })
    .catch(err => {
      console.error('Save error:', err);
    });
  });
});

