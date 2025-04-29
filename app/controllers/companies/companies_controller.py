from flask import Blueprint,request,jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK,HTTP_404_NOT_FOUND,HTTP_403_FORBIDDEN
import validators
from app.models.companies import Company
from app.extensions import db,bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token,jwt_required,get_jwt_identity
from app.models.users import User



#companies Blueprint defining the blueprint
companies = Blueprint('companies', __name__, url_prefix='/api/v1/companies')# defining the prefix for api,version 1 and the table


#Creating companies

@companies.route('/create', methods = ['POST']) #Post is used when creating and registering users and json representaion format []
@jwt_required()
def createCompany(): # creating the company
    #Storing request values
    data = request.json # variable of object storing data
    origin = data.get('origin') #accessing variables from the table
    description = data.get('descrition')
    user_id = get_jwt_identity
    name = data.get('name')
    


#Validations of the incoming request

    if not name or not origin or not description: 
        return jsonify({"error: All fileds are required" }),HTTP_400_BAD_REQUEST
    
    if  Company.query.filter_by(name=name).first() is not None: #Ensuring email and contact constraints 
          return jsonify({"error":"Company name already in use"}),HTTP_409_CONFLICT #Accessing the model to check if the email is valid

    
    try:
       
        #Creating the a new company
        new_company = Company(name=name,origin=origin,description=description,user_id=user_id)
        db.session.add(new_company)
        db.session.commit()


        return jsonify({
            'message': name + " has been successfully ",
            'company':{

                'id':new_company.id,
                'name':new_company.name,
                'origin':new_company.origin,
                'description':new_company.description
            }
        }),HTTP_201_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    

    
#Retrieving all companies    
@companies.get('/')
@jwt_required()
def getAllCompanies():
    try:

        all_companies = Company.query.all()
        companies_data = []
        for company in all_companies:
         company_info = {
            'id': company.id,
            'name': company.name,
            'description': company.description,
            'origin': company.origin,
            'user': {
             'first_name': company.user.first_name,
             'last_name': company.user.last_name,
             'username': company.user.get_full_name(),
             'email': company.user.email,
             'contact': company.user.contact,
             'user_type': company.user.user_type,
             'biography': company.user.biography,
             'created_at': company.user.created_at
    
            },
           'created_at': company.created_at
         }
        companies_data.append(company_info)
        return jsonify({
           "message":"All companies retrieved successfully.",
           "total _companies": len(companies_data),
           "companies": companies_data
        }),HTTP_200_OK

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
        
        
# Get a company By ID
@companies.route('/company/<int:id>')
@jwt_required()
def getCompany(id):
    try:
        company = Company.query.filter_by(id=id).first()

        if not company:
            return jsonify({"error": "Company not found"}), HTTP_404_NOT_FOUND

        return jsonify({
            "message": "Company Details retrieved successfully",
            "company": {
                'id': company.id,
                'name': company.name,
                'description': company.description,
                'origin': company.origin,
                'user': {
                    'first_name': company.user.first_name,
                    'last_name': company.user.last_name,
                    'username': company.user.get_full_name(),
                    'email': company.user.email,
                    'contact': company.user.contact,
                    'user_type': company.user.user_type,
                    'biography': company.user.biography,
                    'created_at': company.user.created_at
                },
                'created_at': company.created_at
            }
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
    #Update companies by id
@companies.route('/edit/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def updateCompanyDetails(id):
    try:
        current_user = get_jwt_identity()
        loggedInUser = User.query.filter_by(id=current_user).first()

        # Get company by ID
        company = Company.query.filter_by(id=id).first()

        if not company:
            return jsonify({"error": "Company not found"}), HTTP_404_NOT_FOUND

        elif loggedInUser.user_type != 'admin' and company.user_id != current_user:
            return jsonify({"error": "You are not authorized to update the company details"}), HTTP_403_FORBIDDEN

        # Store request data
        data = request.get_json()
        name = data.get('name', company.name)
        origin = data.get('origin', company.origin)
        description = data.get('description', company.description)
        contact = data.get('contact', company.user.contact)

        # Check for duplicate contact
        if contact != company.user.contact and User.query.filter_by(contact=contact).first():
            return jsonify({"error": "Contact already exists"}), HTTP_409_CONFLICT

        # Update values
        company.name = name
        company.origin = origin
        company.description = description
        company.user.contact = contact

        db.session.commit()

        return jsonify({
            "message": f"{name}'s details updated successfully.",
            'company': {
                'id': company.id,
                'name': company.name,
                'description': company.description,
                'origin': company.origin,
                'user': {
                    'first_name': company.user.first_name,
                    'last_name': company.user.last_name,
                    'username': company.user.get_full_name(),
                    'email': company.user.email,
                    'contact': company.user.contact,
                    'user_type': company.user.user_type,
                    'biography': company.user.biography,
                    'created_at': company.user.created_at
                },
                'created_at': company.created_at
            }
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR
    
    #Delete a company
@companies.route('/delete/<int:id>',methods = ['DELETE'])
@jwt_required()
def deleteCompany(id):
        try:
        
           current_user = get_jwt_identity()
           loggedInUser = User.query.filter_by(id=current_user).first()
           #Get company by id
           company = Company.query.filter_by(id=id).first()

           if not company:
            return jsonify({"error": "Company not found"}),HTTP_404_NOT_FOUND
           
           elif loggedInUser.user_type!= 'admin' and company.user_id!=current_user:
              return jsonify({"error": "You are not authorized to delete this company"}),HTTP_403_FORBIDDEN
           
           else:
             
              #Delete the associated books
              for book in company.books:
               db.session.delete(book)

              #Deleting the company
               db.session.delete(company)
               db.session.commit()

              
              
              return jsonify({
                 "message": "Company has been deleted successfully",
                }),HTTP_200_OK
        except Exception as e:
         return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
         
