// Include this script in your base.html or a custom JS file
$(document).ready(function () {
  $(window).scroll(function () {
    if ($(window).scrollTop() > 50) {
      $(".navbar").addClass("scrolled");
    } else {
      $(".navbar").removeClass("scrolled");
    }
  });
});

document
  .getElementById("navbar-toggler")
  .addEventListener("click", function () {
    this.classList.toggle("active");
    document.getElementById("navbarNav").classList.toggle("active");
  });
