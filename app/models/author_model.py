
from app.extensions import db
from datetime import datetime


class Author(db.Model) :
    __tablename__ = "authors"
    author_id = db.Column(db.Integer, primary_key=True,autoincrement=True,nullable=False)
    first_name = db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    contact = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(100),nullable=False)
    specialisation = db.Column(db.String(100),nullable=False)
    biography = db.Column(db.String(1000),nullable=False)
    location = db.Column(db.String(100),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    # book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    # company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    # book_id = db.relationship('Book', backref='author', lazy=True)
    # company_id = db.relationship('Company', backref='author', lazy=True)
                           
    
    def __init__(self, first_name , last_name,email , contact,password , specialisation,biography,location,created_at,updated_at):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.contact = contact
        self.password = password
        self.specialisation = specialisation
        self.biography = biography
        self.location = location
        self.created_at = created_at
        self.updated_at = updated_at

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

         
   



    
