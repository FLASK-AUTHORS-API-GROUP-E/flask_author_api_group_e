from flask import Flask
from config import Config
from database import db, init_db
from routes import register_routes

app = Flask(__name__)
app.config.from_object('config.Config')
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///database.db'


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    init_db(app)
    register_routes(app)
    return app