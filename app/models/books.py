from .extensions import db  # Import db after it's initialized in __init__.py
from datetime import datetime

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    price_unit = db.Column(db.String(22), nullable=False, default="UGX")
    isbn = db.Column(db.String(30), nullable=True,unique=True)
    genre = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(22), nullable=False)
    user_id =db.Column(db.Integer,db.ForeignKey("users.id"))
    company_id = db.Column(db.Integer,db.ForeignKey("company.id"))
    user = db.relationship("User",backref="books")
    company = db.relationship("Company",backref="books")
    created = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    def __init__(self, first_name, last_name, email, contact, password, image):
        self.first_name = first_name
        self.last_name = last_name
        self.contact = contact
        self.email = email
        self.password = password
        self.image = image

    def __repr__(self) -> str:
     return f"<Book {self.title}>"

          
