# Handles book CRUD operations
from flask import Blueprint, request, jsonify
from models import Book, db

book_bp = Blueprint('book', __name__)

@book_bp.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201

@book_bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    output = [{'id': book.id, 'title': book.title, 'author': book.author} for book in books]
    return jsonify({'books': output})