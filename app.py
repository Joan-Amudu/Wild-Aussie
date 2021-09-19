import os
import random
import datetime
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
def home():
    posts = list(mongo.db.blog.find().sort("title", 1))
    random.shuffle(posts)
    """
    Find posts from the database and
    render posts randomly on home.html
    """
    return render_template("home.html", posts=posts, page_title="Home")


@app.route("/get_posts")
def get_posts():
    posts = list(mongo.db.blog.find().sort("title", 1))
    return render_template("blog.html", posts=posts, page_title="Blog")


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    posts = list(mongo.db.blog.find(
        {"$text": {"$search": query}}).sort("title", 1))
    """
    Search for posts
    return search results that match title"
    """
    return render_template("blog.html", posts=posts, page_title="Blog")


@app.route("/my_page/<username>", methods=["GET", "POST"])
def my_page(username):
    if "user" not in session:
        return redirect(url_for("login"))

    posts = mongo.db.blog.find()

    if "user" in session:
        return render_template(
            "my_page.html", username=session["user"],
            posts=posts, page_title="My Page")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Check if username already exists in database
    If user exists,
    Ensure hashed password matches user input
    If password matches - login successful
    If password doesnot match,
    User is redirected to login page
    If username doesnot exist,
    Return to login page
    """
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for(
                    "my_page", username=session["user"]))
            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html", page_title="Log In")


@app.route("/logout")
def logout():
    """
    remove user from session cookie
    """
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    check if username already exists in our database,
    if username exists - redirect to register page,
    Otherwise, registration is complete
    And user is put in session cookie
    User redirected to my_page.html
    """
    if request.method == "POST":

        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "email": request.form.get("email").lower(),
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("my_page", username=session["user"]))
    return render_template("register.html", page_title="Register")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Contact Details are safely stored in contact collection in database
    """
    if request.method == "POST":
        contact = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "email": request.form.get("email"),
            "message": request.form.get("message")
        }
        mongo.db.contacts.insert_one(contact)
        flash("Message Sent Successfully!")

    return render_template(
        "contact_us.html", page_title="Contact Us")


@app.route("/create_post", methods=["GET", "POST"])
def create_post():
    """
    if "user" not in session:
        return redirect(url_for("login"))
    """
    if request.method == "POST":
        task = {
            "title": request.form.get("title"),
            "created_by": session["user"],
            "location": request.form.get("location"),
            "image_url": request.form.get("image_url"),
            "date_picker": request.form.get("date_picker"),
            "distance": request.form.get("distance"),
            "grade": request.form.get("grade"),
            "description": request.form.get("description"),
            "date": datetime.datetime.now().strftime("%d %B, %Y")
        }
        mongo.db.blog.insert_one(task)
        flash("Post added successfully")
        return redirect(url_for("create_post"))

    posts = mongo.db.blog.find()
    return render_template("my_page.html", posts=posts, page_title="Create Trek")


@app.route("/show_post/<blog_id>")
def show_post(blog_id):
    """
    Show Trek details
    If post not found in database,
    Return 404 error
    """
    post = mongo.db.blog.find_one_or_404({"_id": ObjectId(blog_id)})

    page_title = post["title"]

    return render_template(
        "show_post.html", post=post, page_title=page_title)


@app.route("/edit_post/<blog_id>", methods=["GET", "POST"])
def edit_post(blog_id):
    """
    Check if User is in session
    Edit post and Update to database
    Bind updated information to card in html
    """
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        edits = {
            "title": request.form.get("title"),
            "created_by": session["user"],
            "location": request.form.get("location"),
            "image_url": request.form.get("image_url"),
            "date_picker": request.form.get("date_picker"),
            "distance": request.form.get("distance"),
            "grade": request.form.get("grade"),
            "description": request.form.get("description"),
            "date": datetime.datetime.now().strftime("%d %B, %Y")
        }
        mongo.db.blog.update({"_id": ObjectId(blog_id)}, edits)
        flash("Post updated successfully")
        return redirect(url_for("my_page", username=session["user"]))

    post = mongo.db.blog.find_one_or_404({"_id": ObjectId(blog_id)})

    posts = mongo.db.blog.find()
    return render_template("edit_post.html", posts=posts, post=post, page_title="Edit Post")


@app.route("/delete_post<blog_id>")
def delete_post(blog_id):
    """
    If user not in session,
    Return user to login page
    Otherise, Delete post
    """
    if "user" not in session:
        return redirect(url_for("login"))

    mongo.db.blog.remove({"_id": ObjectId(blog_id)})
    flash("post deleted successfully")

    return render_template("my_page.html", page_title="Delete Post")


# Error Handlers
@app.errorhandler(404)
def response_404(e):
    return render_template('404.html', page_title="404")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
