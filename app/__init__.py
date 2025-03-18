from flask import Flask
from app.extensions import db,migrate, jwt
from app.controllers.Auth.Auth_controller import auth



# Application Factory
def create_app():
    app = Flask(__name__)
    
    # Load configurations from the config file
    app.config.from_object("config.Config") 

    
    # Initialize the extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


    # Registering models
    from app.models.author_model import Author
    from app.models.book_model import Book
    from app.models.company_model import Company
    

    # Registering blueprints
    app.register_blueprint(auth)



    
    # Index Route
    @app.route('/')
    def index():
        return "Welcome to the API"

    return app

