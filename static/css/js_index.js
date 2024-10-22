const container = document.getElementById('container');
const registerBtn = document.getElementById('register'); // Button on login page
const loginBtn = document.getElementById('registercad'); // Button on signup page

registerBtn.addEventListener('click', () => {
  container.classList.add("active");
  window.location.href = "/register"; // Redirect to signup page (assuming path)
});

loginBtn.addEventListener('click', () => {
  container.classList.remove("active"); // Remove active class to show login form
  window.location.href = "/login"; // Redirect to login page (assuming path)
});
