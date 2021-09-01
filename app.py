import os
import json
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", page_title="Home")


@app.route("/get_posts")
def get_posts():
    posts = list(mongo.db.blog.find().sort("title", 1))
    return render_template("blog.html", posts=posts, page_title="Blog")


@app.route("/my_page/<username>", methods=["GET", "POST"])
def my_page(username):
    # grab the session user's username from database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    posts = mongo.db.blog.find()

    if session["user"]:
        return render_template("my_page.html", username=username, posts=posts)
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # email address will be used as username
        # check if email already exists in our database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed passower matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("my_page", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesnt exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html", page_title="Log In")


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in our database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("my_page", username=session["user"]))
    return render_template("register.html", page_title="Register")


@app.route("/contact")
def contact():
    return render_template("contact_us.html", page_title="Contact Us")


@app.route("/create_post", methods=["GET", "POST"])
def create_post():
    if request.method == "POST":
        task = {
            "title": request.form.get("title"),
            "created_by": session["user"],
            "location": request.form.get("location"),
            "image_url": request.form.get("image_url"),
            "date": request.form.get("date")
        }
        mongo.db.blog.insert_one(task)
        flash("Post added successfully")
        return redirect(url_for("create_post"))

    posts = mongo.db.blog.find()
    return render_template("create_post.html", posts=posts)


@app.route("/edit_post/<blog_id>", methods=["GET", "POST"])
def edit_post(blog_id):
    if request.method == "POST":
        edits = {
            "title": request.form.get("title"),
            "created_by": session["user"],
            "description": request.form.get("description"),
            "image_url": request.form.get("image_url")
        }
        mongo.db.blog.update({"_id": ObjectId(blog_id)}, edits)
        flash("Post updated successfully")

    post = mongo.db.blog.find_one({"_id": ObjectId(blog_id)})

    posts = mongo.db.blog.find()
    return render_template("edit_post.html", posts=posts, post=post)


@app.route("/delete_post<blog_id>")
def delete_post(blog_id):
    mongo.db.blog.remove({"_id": ObjectId(blog_id)})
    flash("post deleted successfully")
    return render_template("my_page.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)  # change to False before submitting
