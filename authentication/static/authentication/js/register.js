document.addEventListener("DOMContentLoaded", function () {
  const passwordField = document.getElementById("passwordField");
  const showPasswordToggle = document.querySelector(".showPasswordToggle");

  // Toggle password visibility
  showPasswordToggle.addEventListener("click", function () {
    const type =
      passwordField.getAttribute("type") === "password" ? "text" : "password";
    passwordField.setAttribute("type", type);

    // Toggle the text between SHOW and HIDE
    this.textContent = type === "password" ? "SHOW" : "HIDE";
  });
});
