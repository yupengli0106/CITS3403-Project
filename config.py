import os

# set secret key
SECRET_KEY = os.environ.get('SECRET_KEY') or 'sshh!'

# get absolute path
basedir = os.path.abspath(os.path.dirname(__file__))

# create database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False