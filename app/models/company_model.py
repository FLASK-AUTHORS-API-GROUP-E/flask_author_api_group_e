from app.extensions import db,migrate
from datetime import datetime

class Company(db.Model):
    __tablename__ = 'company'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    description = db.Column(db.String (10),nullable=False)
    origin = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(345),nullable=False,unique=True)
    contact = db.Column(db.Integer(76),nullable=False,unique=True)
    location = db.Column(db.String(90),nullable=False)
    origin = db.Column(db.String(432),nullable=False)
    created_at =db.Column(db.Datetime, default= datetime.now())
    updated_at = db.Column(db.Datetime, onpdated_at =datetime.now())




class Company :
    def __init__(self,id, name , email , contact , location, Origin, description, created_at, updated_at):
         self.name = name
         self.Origin = Origin
         self.email = email
         self.contact = contact
         self.location = location
         self.description = description
         self.created_at = created_at
         self.updated_at = updated_at

p1= Company('FEEL COMPANY' , 'hawezishakirah@gmail.com' , '0708501678' , 'NAGURU')
print(p1.name)
print(p1.email)
print(p1.contact)
print(p1.location)

print(f'Welcome to {p1.name}, we are located at {p1.location} for more information email us at {p1.email} and you can reach us on {p1.contact}')