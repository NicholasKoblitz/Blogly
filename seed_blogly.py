
from models import db, User, Post
from app import app
from datetime import datetime

# Drops the database if exists and than recreates it
db.drop_all()
db.create_all()

# Deletes data in table if any present
User.query.delete()

# Adds User data
john_doe = User(first_name="John", last_name="Doe")
jane_smith = User(first_name="Jane", last_name="Smith", image_url="https://image.shutterstock.com/image-photo/closeup-portrait-yong-woman-casual-260nw-1554086789.jpg")


# Adds users to db session
db.session.add(john_doe)
db.session.add(jane_smith)

# Commits the session to the db
db.session.commit()

# Deletes data in posts table
Post.query.delete()

# Add posts
post_1 = Post(title="Seed 1", content="This is a seed post!")
post_2 = Post(title="Seed 2", content="Another seed post!!")

# Adds posts to session
db.session.add_all([post_1, post_2])

# Commits posts to db
db.session.commit()