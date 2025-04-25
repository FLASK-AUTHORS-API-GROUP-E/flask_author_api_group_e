from flask import Flask
from app.extensions import db,migrate,jwt
from app.controllers.auth.auth_controller import auth
from app.controllers.users.user_controller import users
from app.controllers.companies.companies_controller import companies


def create_app():

    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)  #  Ensure `migrate` is defined before use
    jwt.init_app(app)  # Initialize JWT

    # Importing and registering the models
    from app.models.users import User
    from app.models.companies import Company
    from app.models.books import Book

    #Registering blueprints
    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(companies)

    @app.route('/')
    def home():
        return 'Welcome to the Authors API!'
    
    return app
