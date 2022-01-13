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

    users = User.query.all()
    return render_template("home_page.html", users=users)


@app.route("/add")
def add_user():
    return render_template("add_user.html")


@app.route("/add-to-db", methods=["POST"])
def add_user_to_db():
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