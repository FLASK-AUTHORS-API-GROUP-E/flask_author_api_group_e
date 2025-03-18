from app.extensions import db
from datetime import datetime

class Company(db.Model):
    __tablename__ = 'company'
    company_id = db.Column(db.Integer, primary_key=True,autoincrement=True,nullable=False)
    name = db.Column(db.String(100),nullable=False)
    origin = db.Column(db.String(200),nullable=False)
    description = db.Column(db.String (10),nullable=False)
    location = db.Column(db.String(90),nullable=False)
    created_at =db.Column(db.DateTime, default= datetime.now)
    updated_at = db.Column(db.DateTime, onupdate = datetime.now)
    # author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    # book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    # author_id = db.relationship('author', backref='company', lazy=True)
    # book_id = db.relationship('Book', backref='company', lazy=True)




class Company :
    def __init__(self,company_id,name,origin,description,location,created_at,updated_at):
         self.company_id = company_id
         self.name = name
         self.origin = origin
         self.description = description
         self.location = location
         self.created_at = created_at
         self.updated_at = updated_at

    