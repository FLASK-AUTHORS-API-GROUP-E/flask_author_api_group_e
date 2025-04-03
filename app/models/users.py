from .extensions import db  # Import db after it's initialized in __init__.py
from datetime import datetime

class User(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(22), nullable=False)
    last_name = db.Column(db.String(22), nullable=False)
    contact = db.Column(db.String(10), nullable=False, unique=True)
    email = db.Column(db.String(22), nullable=False, unique=True)
    image = db.Column(db.String(22), nullable=False)
    password = db.Column(db.String(8), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    def __init__(self, first_name, last_name, email, contact, password, image):
        self.first_name = first_name
        self.last_name = last_name
        self.contact = contact
        self.email = email
        self.password = password
        self.image = image
