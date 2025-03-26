import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/new_item")
def new_item():
    return render_template("new_item.html")

@app.route("/create_item", methods=["POST"])
def create_item():
    title = request.form["title"]
    description = request.form["description"]
    user_id = session["user_id"]
    sql = "INSERT INTO items (title, description, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, description, user_id])
    return redirect("/")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "VIRHE: Anna käyttäjätunnus ja salasana"

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])  

        if not result:
            return "VIRHE: Käyttäjää ei löytynyt"

        user = result[0]
        user_id = user["id"]
        password_hash = user["password_hash"]

        if check_password_hash(password_hash, password):
            session["username"] = username  
            session["user_id"] = user_id
            return redirect("/")
        else:
            return "VIRHE: Väärä tunnus tai salasana"




        
@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")
