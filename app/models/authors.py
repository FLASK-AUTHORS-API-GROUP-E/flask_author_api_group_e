from app.extensions import db
from datetime import datetime

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contact = db.Column(db.String(20), nullable=True)
    user_type = db.Column(db.String(30), nullable=False)
    biography = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return f"<Author {self.first_name} {self.last_name}>"
