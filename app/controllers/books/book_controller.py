from flask import Blueprint, request, jsonify
from app.status_codes import (
    HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK,
    HTTP_404_NOT_FOUND, HTTP_403_FORBIDDEN
)
import validators
from app.models.companies import Company
from app.models.books import Book
from app.models.users import User
from app.extensions import db
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required,
    get_jwt_identity
)

# Books Blueprint
books = Blueprint('books', __name__, url_prefix='/api/v1/books')


# Create a Book
@books.route('/create', methods=['POST'])
@jwt_required()
def createNewBook():
    #Storing request data
    data = request.get_json()

    title = data.get('title')
    pages = data.get('pages')
    price = data.get('price')
    price_unit = data.get('price_unit', 'UGX')  # default to UGX if not provided
    publication_date = data.get('publication_date')
    isbn = data.get('isnb')
    genre = data.get('genre')
    description = data.get('description')
    image = data.get('image')
    company_id = data.get('company_id')
    user_id = get_jwt_identity()

    # Validate required fields
    if not title or not isbn or not description or not price or not price_unit or not genre or not publication_date or not company_id:
        return jsonify({'error': 'All fields are required'}), HTTP_400_BAD_REQUEST
    
    if Book.query.filter_by(title=title,user_id=user_id).first() is not None:
        return jsonify({"error":"Book with this title and user ID already exists"}), HTTP_409_CONFLICT
    if Book.query.filter_by(isbn=isbn).first() is not None:
        return jsonify({"error":"Book isbn already in use"}), HTTP_409_CONFLICT
    
    
    try:
        #Create new book
 

        new_book = Book(
            title=title,
            pages=pages,
            price=price,
            price_unit=price_unit,
            publication_date=publication_date,
            genre=genre,
            description=description,
            isnb=isbn,
            image=image,
            user_id=user_id,
            company_id=company_id
        )

        db.session.add(new_book) 
        db.session.commit()

        return jsonify({
            'message': f"'{title}' has been successfully created.",
            'book': {
                'id': new_book.id,
                'title': new_book.title,
                'pages': new_book.pages,
                'price': new_book.price,
                'price_unit': new_book.price_unit,
                'publication_date': str(new_book.publication_date),
                'genre': new_book.genre,
                'description': new_book.description,
                'isnb': new_book.isnb,
                'image': new_book.image,
                'user_id': new_book.user_id,
                'created_at': str(new_book.created_at),
                'company':{
                    'id':new_book.company.id,
                    'name':new_book.company.name,
                    'origin':new_book.company.origin,
                    'created_at':new_book.company.created_at
                },
                'author':{
                    'first_name':new_book.user.first_name,
                    'last_name':new_book.user.last_name,
                    'first_name':new_book.user.first_name,
                    'username':new_book.user.username,
                    'email':new_book.user.email,
                    'contact':new_book.user.contact,
                    'type':new_book.user.user_type,
                    'biography':new_book.user.biography,
                    'created_at':new_book.user.created_at
                }
            }
        }),HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# Get all books
@books.route('/', methods=['GET'])
@jwt_required()
def getAllBooks():
    try:
        allBooks = Book.query.all()
        booksData = []
        for book in allBooks:
            booksData.append({
                'id': book.id,
                'title': book.title,
                'description': book.description,
                'author': book.author,
                'user': {
                    'first_name': book.user.first_name,
                    'last_name': book.user.last_name,
                    'username': book.user.get_full_name(),
                    'email': book.user.email,
                    'contact': book.user.contact,
                    'user_type': book.user.user_type,
                    'biography': book.user.biography,
                    'created_at': book.user.created_at
                },
                'created_at': book.created_at
            })
        return jsonify({
            "message": "All books retrieved successfully.",
            "total_books": len(booksData),
            "books": booksData
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# Get a book by ID
@books.route('/<int:id>', methods=['GET'])
@jwt_required()
def getBookById(id):
    try:
        book = Book.query.filter_by(id=id).first()
        if not book:
            return jsonify({"error": "Book not found"}), HTTP_404_NOT_FOUND

        return jsonify({
            "message": "Book retrieved successfully",
            "book": {
                'id': book.id,
                'title': book.title,
                'description': book.description,
                'author': book.author,
                'user': {
                    'first_name': book.user.first_name,
                    'last_name': book.user.last_name,
                    'username': book.user.get_full_name(),
                    'email': book.user.email,
                    'contact': book.user.contact,
                    'user_type': book.user.user_type,
                    'biography': book.user.biography,
                    'created_at': book.user.created_at
                },
                'created_at': book.created_at
            }
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# Update a book
@books.route('/edit/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def updateBook(id):
    try:
        current_user = get_jwt_identity()
        loggedInUser = User.query.filter_by(id=current_user).first()

        book = Book.query.filter_by(id=id).first()

        if not book:
            return jsonify({"error": "Book not found"}), HTTP_404_NOT_FOUND

        if loggedInUser.user_type != 'admin' and book.user_id != current_user:
            return jsonify({"error": "You are not authorized to update this book"}), HTTP_403_FORBIDDEN

        data = request.get_json()
        title = data.get('title', book.title)
        description = data.get('description', book.description)
        author = data.get('author', book.author)

        book.title = title
        book.description = description
        book.author = author

        db.session.commit()

        return jsonify({
            "message": f"Book '{title}' updated successfully.",
            "book": {
                'id': book.id,
                'title': book.title,
                'description': book.description,
                'author': book.author,
                'user': {
                    'first_name': book.user.first_name,
                    'last_name': book.user.last_name,
                    'username': book.user.get_full_name(),
                    'email': book.user.email,
                    'contact': book.user.contact,
                    'user_type': book.user.user_type,
                    'biography': book.user.biography,
                    'created_at': book.user.created_at
                },
                'created_at': book.created_at
            }
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# Delete a book
@books.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def deleteBook(id):
    try:
        current_user = get_jwt_identity()
        loggedInUser = User.query.filter_by(id=current_user).first()

        book = Book.query.filter_by(id=id).first()

        if not book:
            return jsonify({"error": "Book not found"}), HTTP_404_NOT_FOUND

        if loggedInUser.user_type != 'admin' and book.user_id != current_user:
            return jsonify({"error": "You are not authorized to delete this book"}), HTTP_403_FORBIDDEN

        db.session.delete(book)
        db.session.commit()

        return jsonify({
            "message": "Book has been deleted successfully"
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
