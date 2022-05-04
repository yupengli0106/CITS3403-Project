from config import app, db
from flask_login import login_user, logout_user, login_required
from flask import render_template, request, flash
from sqlalchemy import func
from models import UserModel, QuestionModel, FileReader
mylist = []  # store question id

@app.route('/')
@app.route('/login.html')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    # clear mylist[] when a new user login
    mylist.clear()
    if request.method == 'POST':
        name = request.form.get('username')
        pwd = request.form.get('password')
        check_remember= request.form.get('remember')
        #username is unique
        user=UserModel.query.filter_by(username=name).first()
        # check if the user existed and the password is correct
        if user is not None and UserModel.decode_password(user.hash_password, pwd):
            curr_user = UserModel()
            curr_user.id = user.id
            curr_user.username = user.username
            # create user 'session'
            login_user(curr_user,remember=check_remember)
            print("user id:", curr_user.username, ' login successful')
            return {'status': 'success'}
        else:
            print('login failed, username or password is incorrect')
            return {'status': 'fail'}
    return render_template('login.html')

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    # clear session
    logout_user()
    return render_template('login.html')

@app.route('/game.html', methods=['POST', 'GET'])
@login_required
def game():
    return render_template('game.html')


@app.route('/register.html', methods=['POST', 'GET'])
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('username')
        pwd = request.form.get('password')
        #username is unique
        user = UserModel.query.filter_by(username=name).first()
        # check if the username is already in the database
        if user is not None:
            print('username already exists')
            flash('Username already exists')
            return {'status': 'fail'}
        # convert password to hash value
        hash_pwd = UserModel.encode_password(pwd)
        print(name, hash_pwd)
        set_user = UserModel(username=name, hash_password=hash_pwd)
        db.session.add(set_user)
        db.session.commit()
        print('register successful')
        return {'status': 'success'}
    return render_template('register.html')

# ramdomly generate a question from QuestionModel and can't be repeated
@app.route('/questions', methods=['POST', 'GET'])
def get_question():
    while True:
        check_question = QuestionModel.query.order_by(func.random()).first()
        if check_question is not None:
            question_id = check_question.id
            ques = check_question.content
            ans = check_question.answer
            if question_id in mylist:
                continue
            mylist.append(question_id)
            print(mylist)
            return {'question': ques, 'answer': ans}


if __name__ == '__main__':
    db.create_all()
    FileReader.read_file(db, 'static/QA.txt')
    app.run(debug=True)

