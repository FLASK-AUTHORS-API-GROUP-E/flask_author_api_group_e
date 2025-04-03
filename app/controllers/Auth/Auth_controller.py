from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED,HTTP_200_OK,HTTP_401_UNAUTHORIZED
from flask_jwt_extended import jwt_required, get_jwt_identity,create_access_token,create_refresh_token
import validators
from app.models.author_model import Author
from app.extensions import db, bcrypt
from werkzeug.security import generate_password_hash

# Auth Blueprint
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

# Author Registration
@auth.route('/register', methods=['POST'])
def register_author():
    try:
        data = request.json

        # Extracting fields from the incoming request
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

        # Check if email or contact already exists
        if Author.query.filter_by(email=email).first():
            return jsonify({"error": "Email address already in use"}), HTTP_409_CONFLICT

        if Author.query.filter_by(contact=contact).first():
            return jsonify({"error": "Contact number already in use"}), HTTP_409_CONFLICT

        # Hash the password using bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create new Author object
        new_author = Author(
            first_name=first_name,
            last_name=last_name,
            password=hashed_password,
            email=email,
            contact=contact,
            biography=biography,
            specialisation=specialisation,
            location=location
        )

        # Save the new author in the database
        db.session.add(new_author)
        db.session.commit()

        # Return success message with author details
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
                "specialisation": new_author.specialisation,
                "location": new_author.location,
                "updated_at": new_author.updated_at,
            }
        }), HTTP_201_CREATED

    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error during registration: {str(e)}")
        db.session.rollback()  # Rollback the transaction if there's an error
        return jsonify({"error": f"An error occurred: {str(e)}"}), HTTP_500_INTERNAL_SERVER_ERROR
    

    #Author Login
@auth.post('/login')
def login():
        email = request.json.get('email')
        password = request.json.get('password')

        try:
            if not password or not email:
                return jsonify({"error": "Email and password are required"}), HTTP_400_BAD_REQUEST
            author = Author.query.filter_by(email=email).first()
            if author:
                is_correct_password = bcrypt.check_password_hash(author.password,password)
                if is_correct_password:
                    access_token = create_access_token(identity = author.author_id)
                    refresh_token = create_refresh_token(identity = author.author_id)
                    return jsonify(access_token=access_token,refresh_token=refresh_token), HTTP_200_OK
                else:
                    return jsonify({"error": "Invalid email or password"}), HTTP_401_UNAUTHORIZED
            
            else:
                        return jsonify({"error": "Invalid email or password"}), HTTP_401_UNAUTHORIZED
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), HTTP_500_INTERNAL_SERVER_ERROR
        
 