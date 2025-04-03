from flask import SQLAlchemy
from flask import Migrate
from flask import Bcrypt
from flask_jwt_extended import JWTManager


migrate = Migrate()
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
