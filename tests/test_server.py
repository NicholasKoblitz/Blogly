from unittest import TestCase
from app import app
from models import User, db

app.config["SQLALCHEMY_DATABASE_URI"] ='postgresql:///blogly_test'
app.config["SQLALCHEMY_ECHO"] = False

app.config["TESTING"] = True

app.config["DEBUG_TB_HOSTS"] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UsersTestCase(TestCase):

    def setUp(self):

        User.query.delete()

        user = User(first_name="John", last_name="Doe", image_url="https://t4.ftcdn.net/jpg/02/14/74/61/360_F_214746128_31JkeaP6rU0NzzzdFC4khGkmqc8noe6h.jpg")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        db.session.rollback()


    def test_home_page(self):
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302)

    def test_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("John Doe", html)

    def test_users_new(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            
            self.assertEqual(resp.status_code, 200)

    def test_users_new_post(self):
        with app.test_client() as client:
            data = {"first_name": "Jane", "last_name": "Doe", "image_url": ""}
            resp = client.post("/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Jane Doe", html)

    def test_user_details(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("John Doe", html)

    def test_user_edit(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edit The User", html)

    def test_users_edit_post(self):
        with app.test_client() as client:
            data = {"first_name": "Jane", "last_name": "Moe", "image_url": ""}
            resp = client.post(f"/users/{self.user_id}/edit", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Jane Moe", html)

    def test_users_delete_post(self):
        with app.test_client() as client:
            data = {"first_name": "John", "last_name": "Doe", "image_url": "https://t4.ftcdn.net/jpg/02/14/74/61/360_F_214746128_31JkeaP6rU0NzzzdFC4khGkmqc8noe6h.jpg"}
            resp = client.post(f"/users/{self.user_id}/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertNotIn("John Doe", html)