# app/__init__.py
from flask import Flask
from app.extensions import db, migrate, jwt  # Import db here
from app.controllers.auth.auth_controller import auth

# Create app instance
def create_app():

  app = Flask(__name__)
  app.config.from_object("config.Config")

  db.init_app(app)
  migrate.init_app(app,db)
  jwt.init_app(app)


#importing models
  from app.models.users import Users
  from app.models.company_model import Company
  from app.models.books import Book

#Registering blue prints
  app.register_blueprint(auth)

  @app.route('/')
  def home():
    return "Authors API"


  return app
