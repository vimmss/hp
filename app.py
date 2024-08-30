from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('honeypot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attempts
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT, ip TEXT, user_agent TEXT, timestamp DATETIME)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']
    captcha = request.form['captcha']
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.now()

    # Check CAPTCHA
    if captcha != "8":  # Simple CAPTCHA validation (5 + 3 = 8)
        return "CAPTCHA failed. Please try again.", 400

    # Log the phishing or spam attempt
    conn = sqlite3.connect('honeypot.db')
    c = conn.cursor()
    c.execute("INSERT INTO attempts (username, password, ip, user_agent, timestamp) VALUES (?, ?, ?, ?, ?)",
              (username, password, ip, user_agent, timestamp))
    conn.commit()
    conn.close()

    # Fake success message
    return "Thank you for logging in!"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
