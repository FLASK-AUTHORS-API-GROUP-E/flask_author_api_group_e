from flask import Blueprint,request,jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK
import validators
from app.models.companies import Company
from app.extensions import db,bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token,jwt_required,get_jwt_identity



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
        
           
        company= Company.query.filter_by(id=id).first()

        if not Company:
            return jsonify({"error": "Company not found"}),HTTP_404_NOT_FOUND
        else:
            return jsonify({
                "message": "Company Details retrieved successfully",
                "company":{
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
            }),HTTP_200_OK

    except Exception as e:
         return jsonify({
            'error': str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
   
    