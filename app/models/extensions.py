from flask import Flask
from flask_sqlalchemy import SQLALchemy
from flask_migrate import Migrate

db = SQLALchemy()
migrate = Migrate()