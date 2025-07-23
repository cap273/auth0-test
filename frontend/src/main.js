document.addEventListener('DOMContentLoaded', () => {
  const loginBtn = document.getElementById('login-btn');
  const signupBtn = document.getElementById('signup-btn');
  const logoutBtn = document.getElementById('logout-btn');
  const greeting = document.getElementById('greeting');
  const userInfo = document.getElementById('user-info');

  function updateUI(user) {
    if (user) {
      greeting.textContent = `Welcome, ${user.name}`;
      loginBtn.style.display = 'none';
      signupBtn.style.display = 'none';
      logoutBtn.style.display = 'inline-block';
      userInfo.textContent = JSON.stringify(user, null, 2);
    } else {
      greeting.textContent = 'Welcome to the App';
      loginBtn.style.display = 'inline-block';
      signupBtn.style.display = 'inline-block';
      logoutBtn.style.display = 'none';
      userInfo.textContent = '';
    }
  }

  fetch('http://localhost:5000/user', { credentials: 'include' })
    .then(res => res.ok ? res.json() : null)
    .then(user => updateUI(user))
    .catch(() => updateUI(null));

  loginBtn.addEventListener('click', () => {
    window.location.href = 'http://localhost:5000/login';
  });

  signupBtn.addEventListener('click', () => {
    window.location.href = 'http://localhost:5000/signup';
  });

  logoutBtn.addEventListener('click', () => {
    window.location.href = 'http://localhost:5000/logout';
  });
});