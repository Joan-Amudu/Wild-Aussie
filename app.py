import os
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
    return render_template("home.html")


@app.route("/get_posts")
def get_posts():
    posts = mongo.db.blog.find()
    return render_template("blog.html", posts=posts)


@app.route("/my_page")
def my_page():
    return render_template("my_page.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    return render_template("logout.html")


@app.route("/register", methods=["GET", "POST"])
"""
register user to database
Code Institute mini project 
"""
def register():
    if request.method == "POST":
        # check if username(email address) already exists in our database
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
    return render_template("register.html")


@app.route("/contact")
def contact():
    return render_template("contact_us.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)  # change to False before submitting
