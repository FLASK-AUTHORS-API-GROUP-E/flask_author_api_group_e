# Handles company CRUD operations
from flask import Blueprint, request, jsonify
from models import Company, db

company_bp = Blueprint('company', __name__)

@company_bp.route('/companies', methods=['POST'])
def create_company():
    data = request.get_json()
    new_company = Company(name=data['name'])
    db.session.add(new_company)
    db.session.commit()
    return jsonify({'message': 'Company added successfully'}), 201

@company_bp.route('/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    output = [{'id': company.id, 'name': company.name} for company in companies]
    return jsonify({'companies': output})