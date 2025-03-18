# Handles company CRUD operations
from flask import Blueprint, request, jsonify
from models import Company, db # Import the Company model and database instance


# Create a Blueprint for handling company-related routes
company_bp = Blueprint('company', __name__)



# Route to create a new company
@company_bp.route('/companies', methods=['POST'])
def create_company():
    data = request.get_json()
    new_company = Company(name=data['name'])
    # Add the new company to the database session and commit changes
    db.session.add(new_company)
    db.session.commit()
    return jsonify({'message': 'Company added successfully'}), 201


# Route to retrieve all companies from the database
@company_bp.route('/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()  # Fetch all companies from the database
    output = [{'id': company.id, 'name': company.name} for company in companies]# Format the retrieved data into a list of dictionaries
    return jsonify({'companies': output})# Return the list of companies in JSON format