import os
import random
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
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
def hello():
    return render_template('login.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print('login request successful')
        name = request.form.get('username')
        pwd = request.form.get('password')
        if(name == None or pwd == None):
            flash('Please enter both username and password')
        check_user=UserModel.query.filter_by(username=name,password=pwd).first()
        if check_user:
            print('login successful')
            return {'status': 'success'}
        else:
            print('login failed')
            return {'status': 'fail'}
    else:
        flash('request unsuccessful')


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
        print(name, pwd)
        if(name == None or pwd == None):
            return {'status': 'fail'}
        user = UserModel(username=name, password=pwd)
        db.session.add(user)
        db.session.commit()
    else:
        flash('request unsuccessful')



@app.route('/question', methods=['POST', 'GET'])
def question():
    num=random.randint(1,100)
    check_question = QuestionModel.query.filter_by(id=1).first()
    ques = check_question.content
    ans = check_question.answer
    return {'question': ques, 'answer': ans}


if __name__ == '__main__':
    app.run(debug=True)
