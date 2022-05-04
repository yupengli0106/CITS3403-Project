import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import  LoginManager


app = Flask(__name__)


# get absolute path
basedir = os.path.abspath(os.path.dirname(__file__))
app.secret_key = "super-secret-keyyyy"

# Configure database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'flask_sql.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.session_protection = "strong"
