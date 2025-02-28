from flask import *
import sqlite3

app = Flask(__name__)




@app.route("/")
def home():
    return render_template("signup.html")

@app.route("/signup_message", methods=["POST"])
def signup():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    try:
        conn = sqlite3.connect("Database/users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        conn.commit()
        conn.close()
        return render_template("result.html", value="Signup Successful!")
    except sqlite3.IntegrityError:
        return render_template("result.html", value="Error: Username or Email already exists!")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_message", methods=["POST"])
def login_message():
    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("Database/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return render_template("api_call.html")
    else:
        return render_template("result.html", value="Invalid Email or Password!")

if __name__ == "__main__":
    app.run(debug=True)
