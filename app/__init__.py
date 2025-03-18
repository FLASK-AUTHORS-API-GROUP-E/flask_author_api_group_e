# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate


# # Extensions
# db = SQLAlchemy()
# migrate = Migrate()

# # Application Factory
# def create_app():
#     app = Flask(__name__)
#     app.config.from_object("config.Config")

#     db.init_app(app)
#     migrate.init_app(app, db)

#     # Registering models
#     from app.models.authors_models import Author
#     from app.models.book_models import Book
#     from app.models.company_models import Company

#     # Index Route
#     @app.route('/')
#     def index():
#         return "Welcome to the API"

#     return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Extensions
db = SQLAlchemy()
migrate = Migrate()

# Application Factory
def create_app():
    app = Flask(__name__)
    
    # Load configurations from the config file
    app.config.from_object("config.Config")
    
    # Initialize the extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Registering models
    from app.models.authors_models import Author
    from app.models.book_models import Book
    from app.models.company_models import Company
    
    # Index Route
    @app.route('/')
    def index():
        return "Welcome to the API"

    return app
