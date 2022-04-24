import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#get absolute path
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# Configure database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'flask_sql.db')
# Disable dynamic tracking of database modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# instantiate database
db = SQLAlchemy(app)


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))


class QuestionModel(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    answer = db.Column(db.String(4))


'''
instantiate database：
   1. Python env: python3
   2. from [yourapplication] import db
    >>> db.create_all()
   3. from [yourapplication] import [Role] //UserModel instead of users
    >>> admin = UserModel(username='admin')
    >>> guest = UserModel(username='guest') 
   4. 
   >>> db.session.add(admin)
   >>> db.session.add(guest)
   >>> db.session.commit() //.seesion.commit()

'''


if __name__ == '__main__':
    # db.drop_all()
    db.create_all()
    admin = UserModel(username='admin',password='admin')
    q1 = QuestionModel(content='question 1 ', answer='1949')
    db.session.add(q1)
    db.session.add(admin)
    db.session.commit()
    # app.run(debug=True)
