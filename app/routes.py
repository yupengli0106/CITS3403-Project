from config import app, db
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, request, flash
from sqlalchemy import func
from models import UserModel, QuestionModel, FileReader
mylist = []  # store question id

@app.route('/')
@app.route('/login.html', methods=['GET', 'POST'])
def index():
    return render_template('login.html')

@app.route('/register.html', methods=['POST', 'GET'])
def register_page():
    return render_template('register.html')

@app.route('/game.html', methods=['POST', 'GET'])
@login_required
def game():
    return render_template('game.html')

@app.route('/profile.html', methods=['POST', 'GET'])
@login_required
def test():
    return render_template('profile.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    # clear mylist[] when a new user login
    mylist.clear()
    if request.method == 'POST':
        name = request.form.get('username')
        pwd = request.form.get('password')
        user=UserModel.query.filter_by(username=name).first()#username is unique
        # check if the user existed and the password is correct
        if user is not None and user.decode_password(pwd):
            curr_user = UserModel()
            curr_user.id = user.id
            curr_user.username = user.username
            # create user 'session'
            login_user(curr_user,remember=request.form.get('remember'))
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

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('username')
        pwd = request.form.get('password')
        user = UserModel.query.filter_by(username=name).first()#username is unique
        # check if the username is already in the database
        if user is not None:
            print('username already exists')
            flash('Username already exists')
            return {'status': 'fail'}
        new_user = UserModel(username=name)
        # convert new user's password to hash value and store it in the database
        new_user.encode_password(pwd)
        print(name, new_user.hash_password)
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            raise e
        print('register successful')
        return {'status': 'success'}
    return render_template('register.html')

@app.route('/questions', methods=['POST', 'GET'])
# ramdomly generate a question from QuestionModel and can't be repeated
def get_question():
    while True:
        question = QuestionModel.query.order_by(func.random()).first()
        if question is not None:
            question_id = question.id
            ques = question.content
            ans = question.answer
            if question_id in mylist:
                continue
            mylist.append(question_id)
            print(mylist)
            return {'question_id':question_id,'question': ques, 'answer': ans}
        return "no more question"

@app.route('/update', methods=['POST', 'GET'])
@login_required
# update current user's profile in database
def update_user():
    if request.method == 'POST':
        new_name = request.form.get('username')
        new_pwd = request.form.get('password')
        user=UserModel.query.filter_by(username=new_name).first()
        if user is not None and user.id != current_user.id:
            print("update failed, user name already exists")
            flash('update failed, user name already exists')
            return {'status': 'fail'}
        current_user.username = new_name
        current_user.encode_password(new_pwd)
        print(current_user.username, current_user.hash_password)
        db.session.commit()
        logout_user()
        print("update successful")
        return {'status': 'success'}
    return render_template('game.html')

@app.route('/delete', methods=['POST', 'GET'])
@login_required
# delete current user from database
def delete_user():
    user = UserModel.query.filter_by(id=current_user.id).first()
    db.session.delete(user)
    try:
        db.session.commit()
    except Exception as e:
        print("delete user failed")
        raise e
    logout_user()
    print("delete user successful")
    return {'status': 'success'}





if __name__ == '__main__':
    db.create_all()
    FileReader.read_file(db, 'static/QA.txt')
    app.run(debug=True)

