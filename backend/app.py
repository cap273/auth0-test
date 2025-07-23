from flask import Flask, jsonify, request, redirect, session, url_for
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
import sqlite3, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.getenv('SECRET_KEY')

# Auth0 configuration
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=os.getenv('AUTH0_CLIENT_ID'),
    client_secret=os.getenv('AUTH0_CLIENT_SECRET'),
    client_kwargs={
        'scope': 'openid profile email',
    },
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

DATABASE = 'users.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    username, email = data['username'], data['email']

    conn = get_db()
    try:
        conn.execute("INSERT INTO user (username, email) VALUES (?, ?)", (username, email))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "User already exists"}), 400
    finally:
        conn.close()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=os.getenv('AUTH0_REDIRECT_URI'))

@app.route('/signup')
def signup():
    return auth0.authorize_redirect(
        redirect_uri=os.getenv('AUTH0_REDIRECT_URI'),
        screen_hint='signup'
    )

@app.route('/callback')
def callback():
    token = auth0.authorize_access_token()
    userinfo = auth0.userinfo()

    print(f'User Token: {token}')
    print("User Info:")
    print(userinfo)

    session['user'] = userinfo

    # Save user info to DB
    conn = get_db()
    sub = userinfo['sub']
    name = userinfo.get('name', '')
    email = userinfo.get('email', '')
    try:
        conn.execute("INSERT OR IGNORE INTO user (username, email) VALUES (?, ?)", (name, email))
        conn.commit()
    finally:
        conn.close()

    return redirect('http://localhost:5173')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(
        f"https://{os.getenv('AUTH0_DOMAIN')}/v2/logout?"
        f"returnTo=http://localhost:5173&"
        f"client_id={os.getenv('AUTH0_CLIENT_ID')}"
    )

@app.route('/user')
def user():
    if 'user' in session:
        return jsonify(session['user'])
    return jsonify(None), 401

@app.route('/authenticated')
def authenticated():
    return jsonify({"authenticated": 'user' in session})

if __name__ == '__main__':
    app.run(debug=True)