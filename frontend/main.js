document.getElementById('login-btn').onclick = () => {
  window.location.href = 'http://localhost:5000/login';
};

document.getElementById('logout-btn').onclick = () => {
  window.location.href = 'http://localhost:5000/logout';
};

document.getElementById('register-btn').onclick = async () => {
  const username = document.getElementById('username').value;
  const email = document.getElementById('email').value;

  try {
    const response = await fetch('http://localhost:5000/register', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ username, email })
    });

    if (!response.ok) {
      const err = await response.json();
      alert('Registration failed: ' + err.error);
    } else {
      alert('Registration successful!');
    }
  } catch (error) {
    alert('An error occurred: ' + error.message);
  }
};

async function fetchUserInfo() {
  try {
    const response = await fetch('http://localhost:5000/user', {
      credentials: 'include'
    });

    if (response.ok) {
      const user = await response.json();
      if (user) {
        document.getElementById('user-info').innerHTML = `
          <p>Welcome, ${user.name}</p>
          <p>${user.email}</p>
        `;
      }
    } else {
      document.getElementById('user-info').innerText = '';
    }
  } catch (error) {
    console.error('Error fetching user:', error);
  }
}

document.addEventListener('DOMContentLoaded', fetchUserInfo);
