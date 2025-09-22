// Dark Mode Toggle
document.getElementById("theme-toggle").addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");
});

// Sticky Header Effect on Scroll
window.addEventListener("scroll", function () {
    const header = document.querySelector("header");
    if (window.scrollY > 50) {
        header.classList.add("scrolled");
    } else {
        header.classList.remove("scrolled");
    }
});

// Project Details Modal
function showProjectDetails(projectName) {
    document.getElementById("project-modal").style.display = "block";
    document.getElementById("project-title").innerText = projectName;
}

function closeModal() {
    document.getElementById("project-modal").style.display = "none";
}

// Contact Form Validation & Success Message
document.getElementById("contactForm").addEventListener("submit", function(e) {
    e.preventDefault();
    // Simple validation
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const message = document.getElementById("message").value.trim();
  
    if (name && email && message) {
      document.getElementById("formResponse").textContent = "Thanks for reaching out! I'll get back to you soon.";
      this.reset();
    } else {
      document.getElementById("formResponse").textContent = "Please fill out all fields.";
      document.getElementById("formResponse").style.color = "red";
    }
  });
  