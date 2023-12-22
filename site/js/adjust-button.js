// raises the readthedocs version button
document.addEventListener("DOMContentLoaded", function () {
  var versionButton = document.querySelector(".rst-current-version");
  if (versionButton) {
    versionButton.style.bottom = "60px"; // Adjust as necessary
  }
});
