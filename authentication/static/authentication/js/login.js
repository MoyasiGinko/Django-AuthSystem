// Toggle Password Visibility
document.addEventListener("DOMContentLoaded", () => {
  const passwordField = document.getElementById("passwordField");
  const toggleVisibility = document.createElement("span");

  toggleVisibility.classList.add("showPasswordToggle");
  toggleVisibility.textContent = "SHOW";
  const formGroup = passwordField.closest(".form-group");

  formGroup.appendChild(toggleVisibility);

  toggleVisibility.addEventListener("click", () => {
    if (passwordField.type === "password") {
      passwordField.type = "text";
      toggleVisibility.textContent = "HIDE";
    } else {
      passwordField.type = "password";
      toggleVisibility.textContent = "SHOW";
    }
  });
});

const form = document.querySelector("form");
if (form) {
  form.addEventListener("submit", (event) => {
    const username = document.getElementById("usernameField").value.trim();
    const password = document.getElementById("passwordField").value.trim();

    if (!username || !password) {
      event.preventDefault(); // Prevent form submission
      alert("Please fill in all fields.");
    }
  });
}
