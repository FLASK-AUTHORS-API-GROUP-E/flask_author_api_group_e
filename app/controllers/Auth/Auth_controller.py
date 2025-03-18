from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_200_OK
import validators
from app.models.author_model import Author
from app.extensions import db, bcrypt
from datetime import datetime

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required


# Auth Blueprint
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
                 


# User Registration
@auth.route('/register', methods=['POST'])
def register_author():

       
    # """Register a new author."""
    data = request.json

    # Extracting fields
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    password = data.get('password')
    biography = data.get('biography', '')  
    specialisation = data.get('specialisation')  # New field
    location = data.get('location') 

    # Validation checks
    if not all([first_name, last_name, contact, email, password, specialisation, location]):
        return jsonify({"error": "All fields are required"}), HTTP_400_BAD_REQUEST

    if not biography:
        return jsonify({"error": "Enter your author biography"}), HTTP_400_BAD_REQUEST

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({"error": "Invalid email format"}), HTTP_400_BAD_REQUEST

    if Author.query.filter_by(email=email).first():
        return jsonify({"error": "Email address already in use"}), HTTP_409_CONFLICT

    if Author.query.filter_by(contact=contact).first():
        return jsonify({"error": "Contact number already in use"}), HTTP_409_CONFLICT

    try:
        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create new author instance
        new_author = Author(
            first_name=first_name,
            last_name=last_name,
            password=hashed_password,
            email=email,
            contact=contact,
            biography=biography,
            specialisation=specialisation,  # Include specialisation
            location=location,  # Include location
            created_at=datetime.now(),  # Set created_at
            updated_at=datetime.now()  # Set updated_at
        )
            

        # Save to database
        db.session.add(new_author)
        db.session.commit()

        return jsonify({
            'message': f"{new_author.get_full_name()} has been successfully created.",
            'author': {
                "author_id": new_author.author_id,
                "first_name": new_author.first_name,
                "last_name": new_author.last_name,
                "email": new_author.email,
                "contact": new_author.contact,
                "biography": new_author.biography,
                "created_at": new_author.created_at,
                "soecialisation": new_author.specialisation,
                "location": new_author.location,
                "updated_at":new_author.updated_at,

            }
        }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# User Login
@auth.route('/login', methods=['POST'])
def login():
    """Authenticate user and generate JWT tokens."""
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), HTTP_400_BAD_REQUEST

        author = Author.query.filter_by(email=email).first()

        if author and bcrypt.check_password_hash(author.password, password):
            access_token = create_access_token(identity=str(author.author_id))
            refresh_token = create_refresh_token(identity=str(author.author_id))

            return jsonify({
                'user': {
                    'id': author.author_id,
                    'authorname': author.get_full_name(),
                    'email': author.email,
                    'access_token': access_token,
                    'refresh_token': refresh_token
                },
                'message': "Login successful."
            }), HTTP_200_OK

        return jsonify({"error": "Invalid email or password"}), HTTP_401_UNAUTHORIZED
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# Refresh Token
@auth.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token."""
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=str(identity))
    return jsonify({'access_token': new_access_token}), HTTP_200_OK

