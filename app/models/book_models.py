from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.extensions import db, migrate

from datetime import datetime


class Book(db.model) :
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    description = db.Column(db.strings(100),nullable=False)
    title = db.Column(db.String (10),nullable=False)
    price = db.Column(db.Integer(209),nullable=False)
    email = db.Column(db.String(234),nullable=False,unique=True)
    contact = db.Column(db.Integer(65),nullable=False,unique=True)
    location = db.Column(db.String(89),nullable=False)
    image = db.Column(db.String(20),nullable=False)
    no_of_pages = db.Column(db.Integers(24),nullable=False)
    publication_date =db.Column(db.Datetime, default = datetime.now())
    


class book :
    def __init__(self,id, title, price, description, image, no_of_pages, price_unit, publication_date, name , email , contact , location):
         self.id = id
         self.name = name
         self.email = email
         self.contact = contact
         self.location = location
         self.publication_date = publication_date
         self.title = title
         self.price = price
         self.description = description
         self.price_unit = price_unit
         self.no_of_pages = no_of_pages
         self.images = image

p1 = book('FEEL COMPANY' , 'nabwireedith18@gmail.com' , '0761539854' , 'BUKOTO')
print(p1.name)
print(p1.email)
print(p1.contact)
print(p1.location)

print(f'Welcome to {p1.name}, we are located at {p1.location} for more information email us at {p1.email} and you can reach us on {p1.contact}')



