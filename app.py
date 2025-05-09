import sqlite3
import secrets
import math
import time
from flask import Flask, abort
from flask import redirect, render_template, request, session, g

import db
import config
import items
import users


app = Flask(__name__)
app.secret_key = config.secret_key

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response

def require_login():
    if "username" not in session:
        abort (403)

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    all_item_count = items.item_count()
    page_count = math.ceil(all_item_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect(f"/{page_count}")

    current_items = items.get_items(page, page_size)
    return render_template("index.html", items=current_items, page=page, page_count=page_count)


@app.route("/new_item")
def new_item():
    require_login()
    classes = items.get_all_res_classes()
    print("DEBUG classes:", classes)
    return render_template("new_item.html", classes = classes)

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
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort (404)
    if item["user_id"] != session["user_id"]:
        abort (403)
    all_classes = items.get_all_res_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in items.get_classes(item_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_item.html", item = item, classes = classes,
                           all_classes = all_classes)

@app.route("/user/<int:user_id>")
def user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort (404)
    print(user)
    items = users.get_items(user_id)
    return render_template("show_user.html", user = user, items = items)

@app.route("/item/<int:item_id>")
def item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort (404)
    print(item)
    classes = items.get_classes(item_id)
    rating_avg = items.get_rating_avg(item_id)
    rating_count = items.get_rating_count(item_id)
    comments = items.get_comments(item_id)
    if comments is None:
        comments = []

    return render_template("show_item.html", item = item, classes = classes, rating_avg = rating_avg,
                           rating_count = rating_count, comments = comments)


@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
    check_csrf()
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    user_id = session["user_id"]

    all_classes = items.get_all_res_classes()


    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            if parts[0] not in all_classes:
                abort(403)
            if parts[1] not in all_classes[parts[0]]:
                abort(403)
            classes.append((parts[0], parts[1]))
    items.add_item(title, description, user_id, classes)
    return redirect("/")

@app.route("/create_rating", methods=["POST"])
def create_rating():
    require_login()
    check_csrf()
    rating = request.form["rating"]
    comment = request.form["comment"]
    print("DEBUG rating:", rating) #debugging
    user_id = session["user_id"]
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not rating or not item:
        abort(403)
    items.add_rating(rating, user_id, item_id, comment)
    return redirect("/")

@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
    check_csrf()
    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort (404)
    if item["user_id"] != session["user_id"]:
        abort (403)
    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    user_id = session["user_id"]

    all_classes = items.get_all_res_classes()


    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            if parts[0] not in all_classes:
                abort(403)
            if parts[1] not in all_classes[parts[0]]:
                abort(403)
            classes.append((parts[0], parts[1]))

    items.update_item(item_id, title, description, classes)
    return redirect("/item/" + str(item_id))


@app.route("/remove_item/<int:item_id>", methods=["POST", "GET"])
def remove_item(item_id):
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort (404)
    if item["user_id"] != session["user_id"]:
        abort (403)
    if request.method == "GET":
        return render_template("remove_item.html", item = item)
    if request.method == "POST":
        check_csrf()
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
    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return redirect("/")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "VIRHE: Anna käyttäjätunnus ja salasana"
        user_id = users.check_login(username, password)

        if user_id:
            session["username"] = username
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            return "VIRHE: Väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "username" in session:
        del session["username"]
        del session["user_id"]
        del session["csrf_token"]
    return redirect("/")

@app.route("/debug_items")
def debug_items():
    sql = "SELECT id, title FROM items"
    result = db.query(sql)
    return "<br>".join([f"{row['id']}: {row['title']}" for row in result])
