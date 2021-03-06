"""Blogly application."""
from crypt import methods
from operator import methodcaller
from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
from datetime import datetime

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

    posts_by_dates = Post.query.filter(
        Post.created_at <= datetime.now()).limit(5)

    tags = PostTag.query.all()

    return render_template("home_page.html", posts=posts_by_dates, tags=tags)


# User Routes
@app.route("/users")
def show_users():

    users = User.query.order_by(User.last_name).all()

    return render_template("users.html", users=users)


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

    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.route("/users/<int:user_id>")
def show_user_details(user_id):
    """Brings user to the User Details page"""

    user = User.query.get(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()

    return render_template("details.html", user=user, posts=posts)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Brings user to the User edit page"""

    user = User.query.get(user_id)

    return render_template("edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_db(user_id):
    """Adds the updated user information to the database"""

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


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Deletes the selected user"""

    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


# Post routes
@app.route("/users/<int:user_id>/posts/new")
def get_post_page(user_id):
    """Loads the create new post page"""

    user = User.query.get(user_id)
    tags = Tag.query.all()

    return render_template("add_post.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Adds user post to database"""

    user = User.query.get(user_id)

    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist("tag_names")

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    for tag in tags:
        add_tag = Tag.query.filter(Tag.name == tag).limit(1)
        post_tag = PostTag(post_id=post.id, tag_id=add_tag[0].id)

        db.session.add(post_tag)
        db.session.commit()

    return redirect(f"/users/{user.id}")


@app.route("/posts/<int:post_id>")
def get_post(post_id):
    """Brings up the post detail page"""

    post = Post.query.get(post_id)
    tags = PostTag.query.filter(PostTag.post_id == post_id).all()
    tag_names = []

    for tag in tags:
        tag_names.append(tag.tags.name)

    return render_template("post.html", post=post, tags=tag_names)


@app.route("/posts/<int:post_id>/edit")
def get_edit_post(post_id):
    """Gets edit post form"""

    post = Post.query.get(post_id)
    tags = Tag.query.all()

    return render_template("edit_post.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """Updates user post"""

    post = Post.query.get(post_id)

    title = request.form["title"]
    content = request.form["content"]

    post.title = title
    post.content = content

    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Deletes user post"""

    post = Post.query.get(post_id)
    user_id = post.user_id

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


# Tag Routes
@app.route("/tags")
def get_tags():
    """Shows the tags page"""

    tags = Tag.query.all()

    return render_template("tags.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def get_tag_details(tag_id):
    """Show tag details"""

    tag = Tag.query.get(tag_id)

    return render_template("tag_details.html", tag=tag)


@app.route("/tags/new")
def get_add_tags():
    """Shows the add tags form"""

    return render_template("add_tags.html")


@app.route("/tags/new", methods=["POST"])
def update_tags_table():
    """Adds new tag to database"""

    tag_name = request.form["tag-name"]

    tag = Tag(name=tag_name)

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/edit")
def get_edit_tag(tag_id):
    """Shows tag edit page"""

    tag = Tag.query.get(tag_id)

    return render_template("edit_tag.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def update_tag(tag_id):
    """Updates database with new tag name"""

    tag = Tag.query.get(tag_id)

    tag_name = request.form["tag-name"]

    tag.name = tag_name

    db.session.add(tag)
    db.session.commit()

    return redirect(f"/tags/{tag.id}")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Deletes tag from database"""

    tag = Tag.query.get(tag_id)
    tag_id = tag.id

    db.session.delete(tag)
    db.session.commit()

    return redirect(f"/tags")
