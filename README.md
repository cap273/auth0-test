# Auth0 + Flask + Vite Web App

A simple app demonstrating Auth0 authentication with a Flask backend and a Vite-powered HTML/CSS/JS frontend.

---

## 0. Initialize database

Initialize the local SQLite database if you have not already. In Windows, `/backend`:

```
sqlite3.exe users.db ".read schema.sql"
```

## 1. Environment Variables

Create a `.env` file in the `backend/` directory using this template:

```env
SECRET_KEY=your-flask-secret-key
AUTH0_CLIENT_ID=your-auth0-client-id
AUTH0_CLIENT_SECRET=your-auth0-client-secret
AUTH0_DOMAIN=your-tenant.auth0.com
AUTH0_REDIRECT_URI=http://localhost:5000/callback
```

## 2. Run the Flask backend

```python
cd backend
python3 -m venv .venv
.venv\Scripts\activate.ps1  # On Linux use: source venv/bin/activate
pip install -r requirements.txt
flask run # Runs on http://localhost:5000
```

## 3. Run the frontend using Vite

```python
cd frontend
npm install
npm run dev # Serves on http://localhost:5173
```

## Auth0 Configuration

In your Auth0 Application settings, set the following:

### Allowed Callback URLs

    http://localhost:5000/callback

### Allowed Logout URLs

    http://localhost:5173

### Allowed Web Origins

    http://localhost:5173

## Test app

- Start the Flask server.
- Start the Vite dev server.
- Open `http://localhost:5173` in your browser.
- Use Login or Sign Up buttons.
- Auth0 redirects back and displays the user info.
- Click Logout to securely log out.