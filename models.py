"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connects to the database"""\
    
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Table"""

    def __repr__(self):
        return f"User: {self.first_name} {self.last_name}"

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String, nullable=True)
    
    # tag = db.relationship("Tag", secondary='posttag', backref='users')
    # post_tag = db.relationship("PostTag", backref='users')


    def get_full_name(self):
        """Users full name"""

        full_name = f"{self.first_name} {self.last_name}"
        return full_name

    # Sets full name property
    full_name = property(get_full_name)


class Post(db.Model):
    """Post Table"""

    def __repr__(self):
        return f"Post: {self.title}, {self.created_at}"

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    users = db.relationship('User', cascade = 'all, delete', backref = "posts")
    tag = db.relationship("Tag", secondary='post_tags', backref='posts')
    post_tag = db.relationship("PostTag", cascade='all, delete', backref='posts')



class Tag(db.Model):
    """Tags Table"""

    def __repr__(self):
        return f"{self.name}"

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, unique = True)
    
    post_tag = db.relationship('PostTag', cascade = 'all, delete', backref='tags')


class PostTag(db.Model):
    """Post Tags Table"""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)


