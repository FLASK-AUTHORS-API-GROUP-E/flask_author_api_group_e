from flask import Flask
from app.extensions import db, migrate, jwt
from app.controllers.auth.auth_controller import auth
from app.controllers.users.user_controller import users
from app.controllers.companies.companies_controller import companies
from app.controllers.books.book_controller import books
from app.controllers.authors.authors_controller import authors

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)  # Ensure `migrate` is defined before use
    jwt.init_app(app)          # Initialize JWT

    # Import models to ensure they are registered with SQLAlchemy
    from app.models.users import User
    from app.models.companies import Company
    from app.models.books import Book
    from app.models.authors import Author
  



    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(companies)
    app.register_blueprint(books)

    @app.route('/')
    def home():
        return 'Welcome to the Authors API!'
    
    return app
