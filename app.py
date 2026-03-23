import os
from flask import Flask, send_from_directory, render_template, request
import sqlite3

app = Flask(__name__)

def is_blocked(inp):
    blocked_chars = [" ", "1", "="]
    for ch in blocked_chars:
        if ch in inp:
            return True
    return False

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UTIL_DIR = os.path.join(BASE_DIR, 'util')

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT,
        password TEXT,
        role TEXT
    )
    """)

    cursor.execute("DELETE FROM users")

    cursor.execute("INSERT INTO users VALUES ('guest', 'guest69', 'guest')")
    cursor.execute("INSERT INTO users VALUES ('admin', 'nfaiue974efhuirlh4378', 'admin')")

    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/the_final_login/", strict_slashes=False, methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # Apply restriction
        if is_blocked(username) or is_blocked(password):
            return "Wrong password"

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # INTENTIONALLY VULNERABLE
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"

        try:
            cursor.execute(query)
            result = cursor.fetchone()
        except:
            return "Database error!"

        conn.close()

        if result:
            if result[2] == "admin":
                return """
                <h1>Admin Access Granted</h1>
                <p>Logs reveal the truth...</p>
                <p><b>Flag Part 4: QWxnb3JpdGhtfQ==</b></p>
                """
            else:
                return "<h1>Logged in as Guest</h1>"

        return "<h1>Login Failed</h1>"

    return render_template("login.html")

@app.route("/robots.txt")
def robots():
    return send_from_directory(UTIL_DIR, "robots.txt")

@app.route("/ligmabolz67/")
def backup():
    nested_path = os.path.join(UTIL_DIR, "ligmabolz67")
    return send_from_directory(nested_path, "backup.txt")

@app.route("/the_token_script")
def token():
    return send_from_directory(UTIL_DIR, "the_token_script")

# Error handling
@app.errorhandler(404)
def file_not_found(e):
    return "Error: The requested file or route was not found.", 404

if __name__ == "__main__":
    if not os.path.exists(UTIL_DIR):
        print(f"WARNING: The directory {UTIL_DIR} does not exist!")

    app.run(host="0.0.0.0", port=10000)
