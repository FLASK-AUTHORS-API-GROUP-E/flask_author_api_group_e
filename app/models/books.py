from app.extensions import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    pages = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Integer, nullable=False)
    price_unit = db.Column(db.String(50), nullable=False,default='UGX')
    publication_date = db.Column(db.Date, nullable=False)
    isnb = db.Column(db.String(30),nullable=True, unique=True)
    genre = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    company_id = db.Column(db.Integer,db.ForeignKey('companies.id'))
    user = db.relationship ('User', backref='companies')
    company = db.relationship ('Company', backref='users')
    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __init__(self,title,price,description):
        super(Book,self).__init__()
        self.title = title
        self.price = price


    def __repr__(self):
     return f' {self.title}'