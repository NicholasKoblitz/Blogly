"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config["SECRET_KEY"] = "001HHUUDSKFUhhqyw56"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def home_page():
    """Brings to the home page"""

    
    return redirect("/users")


@app.route("/users")
def show_users():

    users = User.query.all()
    return render_template("home_page.html", users=users)


@app.route("/users/new")
def add_user():
    """Sends user to the Add New User form"""

    return render_template("add_user.html")


@app.route("/users/new", methods=["POST"])
def add_user_to_db():
    """Addes new user to the database"""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    if(image_url):
        image_url = image_url
    else:
        image_url = None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.route("/users/<int:user_id>")
def show_user_details(user_id):
    """Brings user to the User Details page"""

    user = User.query.get(user_id)

    return render_template("details.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Brings user to the User edit page"""

    user = User.query.get(user_id)

    return render_template("edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_db(user_id):

    user = User.query.get(user_id)

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    if(image_url):
        image_url = image_url
    else:
        image_url = None

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")