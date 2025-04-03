from flask import Blueprint,request,jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK
import validators
from app.models.users import User
from app.extensions import db,bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token,jwt_required,get_jwt_identity



#auth Blueprint defining the blueprint
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')# defining the prefix for api,version 1 and the table


#User registration

@auth.route('/register', methods = ['POST']) #Post is used when creating and registering users and json representaion format []
def register_user(): # registering the user
    #Storing request values
    data = request.json # variable of object storing data
    first_name = data.get('first_name') #accessing variables from the table
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    user_type = data.get('user_type') if 'user_type' in data else "author"
    password = data.get('password')
    image = data.get('image')
    biography = data.get('biography','')  if type == 'author' else ''
    created_at = data.get('created_at')
    updated_at= data.get('updated_at')


#Validations of the incoming request

    if not first_name or not last_name or not contact or not password or not email: 
        return jsonify({"error: All fileds are required" }),HTTP_400_BAD_REQUEST
    
    if type == 'author' and not biography:
        return jsonify({'error': "Enter your author biography"}),HTTP_400_BAD_REQUEST
    
    #The length of the password
    if len(password) < 8: #Password should not be less than 8
        return jsonify({"error": "Password is too short"}),HTTP_400_BAD_REQUEST
    
    if not validators.email(email): 
        return jsonify({"error":"Email is invalid"}),HTTP_400_BAD_REQUEST
    
    #key value pairs representing data to be accesed
    if  User.query.filter_by(email=email).first() is not None: #Ensuring email and contact constraints 
          return jsonify({"error":"Email address already in use"}),HTTP_409_CONFLICT #Accessing the model to check if the email is valid
    
    if User.query.filter_by(contact=contact).first() is not None:
        return jsonify({"error":"Phone number already in use"}),HTTP_409_CONFLICT
    
    try:
        hashed_password  = bcrypt.generate_password_hash('hunter2')# Hashing password to encrypt password,to avoid unauthorised access

        #Creating the user
        new_user = User(first_name=first_name,last_name=last_name,password=hashed_password,email=email,contact=contact,biography=biography,updated_at=updated_at,created_at=created_at,image=image)
        db.session.add(new_user)
        db.session.commit()

         # User name
        username = new_user.get_full_name()


        return jsonify({
            'message': username + 'has been successfully created as an' + new_user.user_type,
            'user':{

                'id':new_user.id,
                'first_name':new_user.first_name,
                'last_name':new_user.last_name,
                'contact':new_user.contact,
                'email':new_user.email,
                'password':new_user.password,
                'biography':new_user.biography,
                'created_at':new_user.created_at
            }
         }),HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    

    
    
    #User login
@auth.post('/login')  # This is implemented in the auth blueprint
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    try:
        if not password or not email:
            return jsonify({'Message': 'Email and password are required'}), HTTP_400_BAD_REQUEST

        user = User.query.filter_by(email=email).first()

        if user:
            # Corrected variable name and comparison
            is_correct_password = bcrypt.check_password_hash(user.password, password)
            
            if is_correct_password:
                access_token = create_access_token(identity=user.id)
                refresh_token = create_refresh_token(identity=user.id)
                return jsonify({
                    'user': {
                        'id': user.id,
                        'username': user.get_full_name(),  # Corrected method call
                        'email': user.email,  # Fixed typo
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'type':user.user_type,
                    },
                    'message':"You have successfully login to your account."
                }), HTTP_200_OK

            else:
                return jsonify({'message': 'Invalid password'}), HTTP_400_BAD_REQUEST

        else:
            return jsonify({'Message': 'Invalid email address'}), HTTP_401_UNAUTHORIZED

    except Exception as e:
        # Log the exception for debugging
        print(f"Error: {str(e)}")
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
    
# Refresh tokens
# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
@auth.route("token/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify({'access_token':access_token})
