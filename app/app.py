import os
import methods
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from models import UserModel, QuestionModel

#get absolute path
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Configure database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'flask_sql.db')
# Disable dynamic tracking of database modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# instantiate database
db = SQLAlchemy(app)

app.secret_key = "super secret key"
db.create_all()


@app.route('/')
def home_page():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print('login request successful')
        name = request.form.get('username')
        pwd = request.form.get('password')
        if(name == None or pwd == None):
            flash('Please enter both username and password')
            return {'status': 'fail'}
        check_user=UserModel.query.filter_by(username=name,password=pwd).first()
        #get hash value of password
        hash_pwd =check_user.password 
        #check if the hash value of password is equal to the input password
        pwd_authentication=methods.decode_password(hash_pwd,pwd) 
        if pwd_authentication:
            print('login successful')
            return {'status': 'success'}
        else:
            print('login failed')
            return {'status': 'fail'}


@app.route('/game', methods=['POST', 'GET'])
def game():
    return render_template('game.html')


@app.route('/register.html', methods=['POST', 'GET'])
def register_page():
    return render_template('register.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        print('register request successful')
        name = request.form.get('username')
        pwd = request.form.get('password')
        # convert password to hash value
        hash_pwd=methods.encode_password(pwd)
        print(name, hash_pwd)
        check_name = UserModel.query.filter_by(username=name).first()#username is unique
        # check if the username is already in the database
        if check_name.username==name:
            print('username already exists')
            flash('Username already exists')
            return {'status': 'fail'}
        if(name == None or pwd == None):
            return {'status': 'fail'}
        user = UserModel(username=name, password=pwd)
        db.session.add(user)
        db.session.commit()
    return {'status': 'success'}


# ramdomly generate a question from QuestionModel and can't be repeated
@app.route('/questions', methods=['POST', 'GET'])
def get_question():
    check_question = QuestionModel.query.order_by(func.random()).first()
    ques = check_question.content
    ans = check_question.answer
    return {'question': ques, 'answer': ans}


if __name__ == '__main__':
    app.run(debug=True)
