from app.extensions import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    price_unit = db.Column(db.String(50), nullable=False, default='UGX')
    publication_date = db.Column(db.Date, nullable=False)
    isbn = db.Column(db.String(30), nullable=True, unique=True)
    genre = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    user = db.relationship('User', backref='books')  # Correct backref
    company = db.relationship('Company', backref='books')  # Correct backref

    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    def __init__(self, title, pages, price, price_unit, publication_date, genre, description, user_id, company_id, isnb=None, image=None):
        self.title = title
        self.pages = pages
        self.price = price
        self.price_unit = price_unit
        self.publication_date = publication_date
        self.genre = genre
        self.description = description
        self.user_id = user_id
        self.company_id = company_id
        self.isnb = isnb
        self.image = image

    def __repr__(self):
        return f'<Book {self.title}>'
