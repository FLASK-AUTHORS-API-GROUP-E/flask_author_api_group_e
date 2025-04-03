from flask import Blueprint,request,jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK,HTTP_403_FORBIDDEN,HTTP_404_NOT_FOUND
import validators
from app.models.users import User
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token,jwt_required,get_jwt_identity
from app.extensions import db,bcrypt


#users Blueprint defining the blueprint
users = Blueprint('users', __name__, url_prefix='/api/v1/users')# defining the prefix for api,version 1 and the table


#Retrieving all users from the database
@users.get('/')
def getAllUsers():

    try:

        all_users = User.query.all()
        users_data = []
        for user in all_users:
         user_info = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.get_full_name(),
            'email': user.email,
            'contact': user.contact,
            'user_type': user.user_type,
            'created_at': user.created_at
        }
         users_data.append(user_info)
        return jsonify({
           "message":"All users retieved successfully.",
           "total _users": len(users),
           "users": users_data
        }),HTTP_200_OK

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR


    
    #Retrieving all authors from the database

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
         if hasattr(author,'books' ):
            author_info['books']=[{
               'id': book.id, 
               'title': book.title,
               'price_unit': book.price_unit,
               'description': book.description, 
               'genre': book.genre, 
               'publication_date': book.publication_date, 
               'image': book.image, 
               'created_at': book.created_at,
            } for book in author.books] 

            if hasattr(author,'companies' ):
              author_info['companies']=[{
               'id': company.id, 
               'name': company.name, 
               'origin': company.origin, 
            } for company in author.companies]
         authors_data.append(author_info)
        return jsonify({
           "message":"All authors retrieved successfully.",
           "total _users": len(authors_data),
           "authors": authors_data
        }),HTTP_200_OK

       except Exception as e:
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
       

       #Get a user by id
@users.get('/user/<int:id>')
@jwt_required()
def getUser():
        try:

           user = User.query.filter_by(id=id).first()
           books = []
           companies = []
           if hasattr(user,'books' ):
            books=[{
               'id': book.id, 
               'title': book.title,
               'price_unit': book.price_unit,
               'description': book.description, 
               'genre': book.genre, 
               'publication_date': book.publication_date, 
               'image': book.image, 
               'created_at': book.created_at,
            } for book in user.books] 

            if hasattr(user,'companies' ):
              companies=[{
               'id': company.id, 
               'name': company.name, 
               'origin': company.origin, 
            } for company in user.companies]
         
           return jsonify({
           "message":"All authors retrieved successfully.",
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
        }),HTTP_200_OK
        except Exception as e:
         return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
    
#Updates the user details
@users.route('/edit/<int:id>',methods = ['PUT','PATCH'])
@jwt_required()
def updateUserDetails():
        try:
           current_user = get_jwt_identity()
           loggedInUser = user.query.filter_by(id=current_user).first()
           #Get uder by id
           user = User.query.filter_by(id=id).first()

           if not user:
            return jsonify({"error": "User not found"}),HTTP_404_NOT_FOUND
           
           elif loggedInUser.user_type!= 'admin' and user.id!=current_user:
              return jsonify({"error": "You are not authorized to update the user details"}),HTTP_403_FORBIDDEN
           
           else:
              #Store request data
              first_name = request.get_json().get('first_name',user.first_name)
              last_name = request.get_json().get('last_name',user.last_name)
              email = request.get_json().get('email',user.email)
              contact =request.get_json().get('contact',user.contact)
              image = request.get_json().get('image',user.image)
              biography = request.get_json().get('biography',user.biography)
              user_type = request.get_json().get('user_type',user.user_type)

              if "password" in request.json:
                 hashed_password = bcrypt.generate_password_hash(request.json('password'))
                 user.password = hashed_password

              if email!=user.email and User.query.filter_by(email=email).first():
               return jsonify({"error": "Email already exists"}), HTTP_409_CONFLICT
              
              if contact!=user.contact and User.query.filter_by(contact=contact).first():
               return jsonify({"error": "Contact already exists"}), HTTP_409_CONFLICT
             
              user.first_name = first_name
              user.last_name = last_name
              user.email = email
              user.contact = contact
              user.biography = biography
              user.user_type = user_type

              db.session.commit()

              username = user.get_full_name()
              
              return jsonify({
                 "message": username + "'s details updated successfully.",
                  'user':{
                     'id': user.id,
                     'first_name': user.first_name,
                     'last_name': user.last_name,
                     'email': user.email,
                     'contact': user.contact,
                     'type': user.user_type,
                     'biography': user.biography,
                     'updated_at': user.updated_at
                    }
              }),HTTP_200_OK
        
        except Exception as e:
         return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
    

#Delete the user 
@users.route('/delete/<int:id>',methods = ['DELETE'])
@jwt_required()
def deleteUser(id):
        try:
        
           current_user = get_jwt_identity()
           loggedInUser = user.query.filter_by(id=current_user).first()
           #Get uder by id
           user = User.query.filter_by(id=id).first()

           if not user:
            return jsonify({"error": "User not found"}),HTTP_404_NOT_FOUND
           
           elif loggedInUser.user_type!= 'admin':
              return jsonify({"error": "You are not authorized to delete this user"}),HTTP_403_FORBIDDEN
           
           else:
             
              #Delete the associated companies
              for company in user.companies:
               db.session.delete(company)

               #Delete the associated books
              for book in user.books:
               db.session.delete(book)

               #Deleting the user
               db.session.delete(user)
               db.session.commit()

              username = user.get_full_name()
              
              return jsonify({
                 "message": "User deleted successfully",
                }),HTTP_200_OK
        except Exception as e:
         return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
    


    

