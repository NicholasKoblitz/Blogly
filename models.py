"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connects to the database"""\
    
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Table"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String, nullable=True)
    

    def get_full_name(self):
        """Users full name"""

        full_name = f"{self.first_name} {self.last_name}"
        return full_name

    # Sets full name property
    full_name = property(get_full_name)