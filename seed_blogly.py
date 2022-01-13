"""Seed file to create and populate blogly database"""

from models import db, User
from app import app


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