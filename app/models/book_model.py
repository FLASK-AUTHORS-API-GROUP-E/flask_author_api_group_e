
from app.extensions import db
from datetime import datetime


class Book(db.Model) :
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True,autoincrement=True,nullable=False)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(10),nullable=False)
    description = db.Column(db.String(100),nullable=False)
    image = db.Column(db.String(256),nullable=False)
    no_of_pages = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Integer,nullable=False)
    publication_date =db.Column(db.String(90),nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime,onupdate=datetime.now)
    # author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)# foreign key
    # company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)# foreign key
    # author = db.relationship('Author', backref='books', lazy=True) # relationship
    # company = db.relationship('Company', backref='books', lazy=True)# relationship


    # # FOREIGN KEY
    # author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    # company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)


    # # RELATIONSHIPS
    # author = db.relationship('Author', backref='books', lazy=True) # relationship
    # company = db.relationship('Company', backref='books', lazy=True)# relationship


class Book :
    def __init__(self,book_id, name,title, price, description, image, no_of_pages, publication_date,created_at,updated_at):
         self.book_id = book_id
         self.name = name
         self.title = title
         self.description = description
         self.image = image
         self.no_of_pages = no_of_pages
         self.price = price
         self.publication_date = publication_date
         self.created_at = created_at
         self.updated_at = updated_at
        

    
