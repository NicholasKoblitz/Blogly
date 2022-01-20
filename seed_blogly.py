
from distutils.command.build_scripts import first_line_re
from models import db, User, Post, Tag, PostTag
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
mike_johnson = User(first_name="Mike", last_name="Johnson", image_url="https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500")
sabrina_soo = User(first_name="Sabrina", last_name="Soo")


# Adds users to db session
db.session.add_all([john_doe, jane_smith, mike_johnson, sabrina_soo])

# Commits the session to the db
db.session.commit()

# Deletes data in posts table
Post.query.delete()

# Add posts
post_1 = Post(title="Seed 1", content="This is a seed post!", user_id=1)
post_2 = Post(title="Seed 2", content="Another seed post!!", user_id=2)
post_3 = Post(title="First Post", content="Hello, this is my first post. How are you all?", user_id=3)
post_4 = Post(title="Life Update", content="All is going GOOD!!", user_id=1)
post_5 = Post(title="Workers Needed!", content="If you want to work call me", user_id=4)
# Adds posts to session
db.session.add_all([post_1, post_2, post_3, post_4, post_5])

# Commits posts to db
db.session.commit()


# Deletes data in table if any exists
Tag.query.delete()

# Adds Tags to the database
funny = Tag(name='Funny')
cool = Tag(name='Cool')
sad = Tag(name="Sad")
cat = Tag(name="Cat")

# Adds data to db session
db.session.add_all([funny, cool, sad, cat])

# Commits data to db
db.session.commit()

# Deletes any data in table
PostTag.query.delete()

# Creates tags
funny_tag = PostTag(post_id=1, tag_id=1)
cat_tag = PostTag(post_id=3, tag_id=4)

# Adds tags to database
db.session.add_all([funny_tag, cat_tag])


db.session.commit()