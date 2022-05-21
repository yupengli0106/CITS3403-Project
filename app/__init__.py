from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import  LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')

# create database object
db = SQLAlchemy(app)

# Configure migrate
db.init_app(app)
migrate = Migrate(app, db)

# Configure login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = "strong"

from app import routes, models

