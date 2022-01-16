from unittest import TestCase
from app import app
from models import User, Post, db

app.config["SQLALCHEMY_DATABASE_URL"] ='postgresql:///blogly_test'
app.config["SQLALCHEMY_ECHO"] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):

    def setUp(self):

        User.query.delete()

    def tearDown(self):

        db.session.rollback()

    def test_get_full_name(self):
        user = User(first_name="John", last_name="Doe", image_url="https://t4.ftcdn.net/jpg/02/14/74/61/360_F_214746128_31JkeaP6rU0NzzzdFC4khGkmqc8noe6h.jpg")

        full_name = user.get_full_name()
        self.assertEqual(full_name, "John Doe")

        
    def test_full_name_property(self):
        user = User(first_name="John", last_name="Doe", image_url="https://t4.ftcdn.net/jpg/02/14/74/61/360_F_214746128_31JkeaP6rU0NzzzdFC4khGkmqc8noe6h.jpg")

        full_name = user.full_name
        self.assertEqual(full_name, "John Doe")

    def test_relationship(self):
        user = User(first_name="John", last_name="Doe", image_url="https://t4.ftcdn.net/jpg/02/14/74/61/360_F_214746128_31JkeaP6rU0NzzzdFC4khGkmqc8noe6h.jpg")

        post = Post(title="TEST POST", content="This is a test", user_id=user.id)
    
        self.assertEqual(post.user_id, user.id)
