from unittest import TestCase
from app import app
from models import db, User, Post, Tag, PostTag

app.config["SQLALCHEMY_DATABASE_URL"] = 'postgresql:///blogly_test'
app.config["SQLALCHEMY_ECHO"] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):

    def setUp(self):

        User.query.delete()

        user = User(first_name="John", last_name="Doe",
                    image_url="https://t4.ftcdn.net/jpg/02/14/74/61/360_F_214746128_31JkeaP6rU0NzzzdFC4khGkmqc8noe6h.jpg")

    def tearDown(self):

        db.session.rollback()

    def test_get_full_name(self):

        full_name = self.user.get_full_name()
        self.assertEqual(full_name, "John Doe")

    def test_full_name_property(self):
        # user = User(first_name="John", last_name="Doe", image_url="https://t4.ftcdn.net/jpg/02/14/74/61/360_F_214746128_31JkeaP6rU0NzzzdFC4khGkmqc8noe6h.jpg")

        full_name = self.user.full_name
        self.assertEqual(full_name, "John Doe")

    def test_relationship_user_to_post(self):
        # user = User(first_name="John", last_name="Doe", image_url="https://t4.ftcdn.net/jpg/02/14/74/61/360_F_214746128_31JkeaP6rU0NzzzdFC4khGkmqc8noe6h.jpg")

        post = Post(title="TEST POST", content="This is a test",
                    user_id=self.user.id)

        self.assertEqual(post.user_id, self.user.id)

    def test_relationship_post_to_tag(self):
        tag = Tag(name="Test 1")
        post = Post(title="TEST POST", content="This is a test",
                    user_id=self.user.id)

        self.assertEqual(tag.name, post.tag.name)

    def test_relationship_post_to_post_tag(self):
        post = Post(title="TEST POST", content="This is a test",
                    user_id=self.user.id)
        tag = Tag(name="Test 1")
        tag_post = PostTag(post_id=1, tag_id=1)

        self.assertEqual(post.id, post.post_tag.post_id)
        self.assertEqual(tag.id, tag.post_tag.tag_id)
