# Registers all routes from controllers
from flask import Flask
from controllers.auth.auth_controller import auth_bp
from controllers.book.book_controller import book_bp
from controllers.company.company_controller import company_bp

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(book_bp, url_prefix='/books')
    app.register_blueprint(company_bp, url_prefix='/companies')