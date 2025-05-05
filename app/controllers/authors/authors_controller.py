from flask import Blueprint, request, jsonify
from app.status_codes import (
    HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK,
    HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
)
import validators
from app.models.users import User
from app.models.books import Book
from app.extensions    import db

from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from app.extensions import db, bcrypt

# Auth Blueprint
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# Register Author
@auth.route('/register', methods=['POST'])
def register_user():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    user_type = data.get('user_type') if 'user_type' in data else "author"
    password = data.get('password')
    image = data.get('image')
    biography = data.get('biography', '') if user_type == 'author' else ''
    created_at = data.get('created_at')
    updated_at = data.get('updated_at')

    if not first_name or not last_name or not contact or not password or not email:
        return jsonify({"error": "All fields are required"}), HTTP_400_BAD_REQUEST

    if user_type == 'author' and not biography:
        return jsonify({'error': "Enter your author biography"}), HTTP_400_BAD_REQUEST

    if len(password) < 8:
        return jsonify({"error": "Password is too short"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({"error": "Email is invalid"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email address already in use"}), HTTP_409_CONFLICT

    if User.query.filter_by(contact=contact).first() is not None:
        return jsonify({"error": "Phone number already in use"}), HTTP_409_CONFLICT

    try:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            password=hashed_password,
            email=email,
            contact=contact,
            biography=biography,
            user_type=user_type,
            updated_at=updated_at,
            created_at=created_at,
            image=image
        )
        db.session.add(new_user)
        db.session.commit()

        username = new_user.get_full_name()

        return jsonify({
            'message': f"{username} has been successfully created as an {new_user.user_type}",
            'user': {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'contact': new_user.contact,
                'email': new_user.email,
                'biography': new_user.biography,
                'created_at': new_user.created_at
            }
        }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Login Author
@auth.post('/login')
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    try:
        if not password or not email:
            return jsonify({'message': 'Email and password are required'}), HTTP_400_BAD_REQUEST

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return jsonify({
                'user': {
                    'id': user.id,
                    'username': user.get_full_name(),
                    'email': user.email,
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'type': user.user_type,
                },
                'message': "You have successfully logged in."
            }), HTTP_200_OK

        return jsonify({'message': 'Invalid email or password'}), HTTP_401_UNAUTHORIZED

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Refresh Access Token
@auth.route("/token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token': access_token})

# Define blueprint
users = Blueprint('users', __name__, url_prefix='/api/v1/users')

# Get all users
@users.get('/')
def getAllUsers():
    try:
        all_users = User.query.all()
        users_data = [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.get_full_name(),
            'email': user.email,
            'contact': user.contact,
            'user_type': user.user_type,
            'created_at': user.created_at
        } for user in all_users]

        return jsonify({
            "message": "All users retrieved successfully.",
            "total_users": len(users_data),
            "users": users_data
        }), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Get all authors
@users.get('/authors')
@jwt_required()
def getAllAuthors():
    try:
        all_authors = User.query.filter_by(user_type='author').all()
        authors_data = []
        for author in all_authors:
            author_info = {
                'id': author.id,
                'first_name': author.first_name,
                'last_name': author.last_name,
                'username': author.get_full_name(),
                'email': author.email,
                'contact': author.contact,
                'biography': author.biography,
                'created_at': author.created_at,
                'companies': [],
                'books': []
            }
            if hasattr(author, 'books'):
                author_info['books'] = [{
                    'id': book.id,
                    'title': book.title,
                    'price_unit': book.price_unit,
                    'description': book.description,
                    'genre': book.genre,
                    'publication_date': book.publication_date,
                    'image': book.image,
                    'created_at': book.created_at
                } for book in author.books]
            if hasattr(author, 'companies'):
                author_info['companies'] = [{
                    'id': company.id,
                    'name': company.name,
                    'origin': company.origin
                } for company in author.companies]
            authors_data.append(author_info)
        return jsonify({
            "message": "All authors retrieved successfully.",
            "total_authors": len(authors_data),
            "authors": authors_data
        }), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Get author by ID
@users.get('/user/<int:id>')
@jwt_required()
def getUser(id):
    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            return jsonify({'error': 'User not found'}), HTTP_404_NOT_FOUND

        books = [{
            'id': book.id,
            'title': book.title,
            'price_unit': book.price_unit,
            'description': book.description,
            'genre': book.genre,
            'publication_date': book.publication_date,
            'image': book.image,
            'created_at': book.created_at
        } for book in getattr(user, 'books', [])]

        companies = [{
            'id': company.id,
            'name': company.name,
            'origin': company.origin
        } for company in getattr(user, 'companies', [])]

        return jsonify({
            "message": "User retrieved successfully.",
            "user": {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.get_full_name(),
                'email': user.email,
                'contact': user.contact,
                'user_type': user.user_type,
                'biography': user.biography,
                'created_at': user.created_at,
                'companies': companies,
                'books': books
            }
        }), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Update user details
@users.route('/edit/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def updateUserDetails(id):
    try:
        current_user = get_jwt_identity()
        loggedInUser = User.query.filter_by(id=current_user).first()
        user = User.query.filter_by(id=id).first()

        if not user:
            return jsonify({"error": "User not found"}), HTTP_404_NOT_FOUND

        if loggedInUser.user_type != 'admin' and user.id != current_user:
            return jsonify({"error": "Not authorized"}), HTTP_403_FORBIDDEN

        data = request.json
        if "password" in data:
            user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        for field in ['first_name', 'last_name', 'email', 'contact', 'image', 'biography', 'user_type']:
            if field in data:
                setattr(user, field, data[field])

        if user.email != data.get('email', user.email) and User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already exists"}), HTTP_409_CONFLICT

        if user.contact != data.get('contact', user.contact) and User.query.filter_by(contact=data['contact']).first():
            return jsonify({"error": "Contact already exists"}), HTTP_409_CONFLICT

        db.session.commit()

        return jsonify({
            "message": f"{user.get_full_name()}'s details updated successfully.",
            "user": {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'contact': user.contact,
                'user_type': user.user_type,
                'biography': user.biography,
                'updated_at': user.updated_at
            }
        }), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Delete user
@users.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def deleteUser(id):
    try:
        current_user = get_jwt_identity()
        loggedInUser = User.query.filter_by(id=current_user).first()
        user = User.query.filter_by(id=id).first()

        if not user:
            return jsonify({"error": "User not found"}), HTTP_404_NOT_FOUND

        if loggedInUser.user_type != 'admin':
            return jsonify({"error": "Not authorized"}), HTTP_403_FORBIDDEN

        for book in getattr(user, 'books', []):
            db.session.delete(book)
        for company in getattr(user, 'companies', []):
            db.session.delete(company)

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted successfully"}), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR

# Search authors
@users.get('/search')
@jwt_required()
def searchAuthors():
    try:
        query = request.args.get('query', '')
        authors = User.query.filter(
            ((User.first_name.ilike(f"%{query}%")) | (User.last_name.ilike(f"%{query}%"))) & (User.user_type == 'author')
        ).all()

        if not authors:
            return jsonify({'message': "No results found"}), HTTP_404_NOT_FOUND

        authors_data = []
        for author in authors:
            author_info = {
                'id': author.id,
                'first_name': author.first_name,
                'last_name': author.last_name,
                'username': author.get_full_name(),
                'email': author.email,
                'contact': author.contact,
                'biography': author.biography,
                'created_at': author.created_at,
                'companies': [],
                'books': []
            }
            if hasattr(author, 'books'):
                author_info['books'] = [{
                    'id': book.id,
                    'title': book.title,
                    'price_unit': book.price_unit,
                    'description': book.description,
                    'genre': book.genre,
                    'publication_date': book.publication_date,
                    'image': book.image,
                    'created_at': book.created_at
                } for book in author.books]
            if hasattr(author, 'companies'):
                author_info['companies'] = [{
                    'id': company.id,
                    'name': company.name,
                    'origin': company.origin
                } for company in author.companies]
            authors_data.append(author_info)

        return jsonify({
            "message": f"Authors with name '{query}' retrieved successfully.",
            "total_search": len(authors_data),
            "search_results": authors_data
        }), HTTP_200_OK
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR