import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import items

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_items = items.get_items()
    print(all_items)
    return render_template("index.html", items = all_items)


@app.route("/new_item")
def new_item():
    return render_template("new_item.html")

@app.route("/find_item")
def find_item():
    query = request.args.get("query")
    if  query:
        results = items.find_items(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query = query, results = results)

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    item = items.get_item(item_id)
    return render_template("edit_item.html", item = item)


@app.route("/item/<int:item_id>")
def item(item_id):
    item = items.get_item(item_id)
    print(item)
    return render_template("show_item.html", item = item)


@app.route("/create_item", methods=["POST"])
def create_item():
    title = request.form["title"]
    description = request.form["description"]
    user_id = session["user_id"]

    items.add_item(title, description, user_id)

    return redirect("/")

@app.route("/update_item", methods=["POST"])
def update_item():
    item_id = request.form["item_id"]
    title = request.form["title"]
    description = request.form["description"]
    user_id = session["user_id"]

    items.update_item(item_id, title, description)

    return redirect("/item/" + str(item_id))


@app.route("/remove_item/<int:item_id>", methods=["POST", "GET"])
def remove_item(item_id):
    if request.method == "GET":
        item = items.get_item(item_id)
        return render_template("remove_item.html", item = item)
    if request.method == "POST":
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))

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
