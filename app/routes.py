from app import app, db
from flask_login import login_user, logout_user, login_required, current_user
from flask import render_template, request, flash, redirect
from sqlalchemy import func
from app.models import UserModel, QuestionModel, ScoreModel

# ---------------------HTML pages-----------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/')
@app.route('/login.html', methods=['GET', 'POST'])
def login_page():
    return render_template('login.html')

@app.route('/register.html', methods=['POST', 'GET'])
def register_page():
    return render_template('register.html')

@app.route('/game.html', methods=['POST', 'GET'])
@login_required
def game_page():
    return render_template('game.html')

@app.route('/profile.html', methods=['POST', 'GET'])
@login_required
def profile_page():
    return render_template('profile.html')

@app.route('/admin_login.html', methods=['POST', 'GET'])
def admin_login_page():
    return render_template('admin_login.html')

@app.route('/admin_index.html', methods=['POST', 'GET'])
@login_required
def admin_index_page():
    return render_template('admin_index.html')

# ---------------------basic functions-----------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form.get('username')
        pwd = request.form.get('password')
        user=UserModel.query.filter_by(username=name).first()#username is unique
        # check if the user existed and the password is correct
        if user is not None and user.decode_password(pwd) and not user.admin:
            curr_user = UserModel()
            curr_user.id = user.id
            curr_user.username = user.username
            login_user(curr_user,remember=request.form.get('remember'))
            print("user id:", curr_user.username, ' login successful')
            return {'status': 'success'}
        print('login failed, username or password is incorrect')
        return {'status': 'fail'}
    return render_template('login.html')

@app.route('/admin_login', methods=['POST', 'GET'])
def admin_login():
    if request.method == 'POST':
        name = request.form.get('username')
        pwd = request.form.get('password')
        user = UserModel.query.filter_by(username=name).first()
        if user is not None and user.decode_password(pwd) and user.admin:
            curr_user = UserModel()
            curr_user.id = user.id
            curr_user.username = user.username
            login_user(curr_user, remember=request.form.get('remember'))
            return {'status': 'success'}
        print('login failed, username or password is incorrect')
        return {'status': 'fail'}
    return render_template('admin_login.html')

@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect('/login.html')

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
@login_required
# ramdomly generate a question from QuestionModel
def get_question():
    while True:
        question = QuestionModel.query.order_by(func.random()).first()
        if question is not None:
            question_id = question.id
            ques = question.content
            ans = question.answer
             # if the user has answered all the questions then return game over
            if ScoreModel.query.filter_by(user_id=current_user.id).count() == QuestionModel.query.count():
                return {'status': 'game_over'}
             # check if the question has been answered correctly by the user
            if ScoreModel.query.filter_by(user_id=current_user.id, ques_id=question.id).first() is not None:
                continue
            return {'question_id':question_id,'question': ques, 'answer': ans}
        return {'status': 'fail'}

# ---------------------user profile-----------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/update', methods=['POST', 'GET'])
@login_required
# update current user's profile in database
def update_user():
    if request.method == 'POST':
        new_name = request.form.get('username')
        new_pwd = request.form.get('password')
        user=UserModel.query.filter_by(username=new_name).first()
        # check if the username is already existed (excluding current user's name)
        if user is not None and user.id != current_user.id:
            print("update failed, user name already exists")
            flash('update failed, user name already exists')
            return {'status': 'fail'}
        current_user.username = new_name
        current_user.encode_password(new_pwd)
        print(current_user.username, current_user.hash_password)
        try:
            db.session.commit()
        except Exception as e:
            raise e
        logout_user()
        print("update successful")
        return {'status': 'success'}
    return render_template('game.html')

@app.route('/delete', methods=['POST', 'GET'])
@login_required
# delete current user from database
def delete_user():
    user = UserModel.query.filter_by(id=current_user.id).first()
    user_records = ScoreModel.query.filter_by(user_id=current_user.id).all()
    if user_records is not None:
        # delete all records of current user
        for record in user_records:
            db.session.delete(record)
    # delete current user
    db.session.delete(user)
    try:
        db.session.commit()
    except Exception as e:
        print("delete user failed")
        raise e
    logout_user()
    print("delete user successful")
    return {'status': 'success'}

# ---------------------share function-----------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/statistic', methods=['POST', 'GET'])
def user_statistic():
    if request.method == 'POST':
        ques_id = request.form.get('question_id')
        #check how many times the user entered the answer (0 < streak <= 6)
        streak = request.form.get('streak')
        # A new record is added to the database each time the user answers a question correctly
        user = ScoreModel(user_id=current_user.id, ques_id=ques_id, score=int(6/streak))
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            raise e
    return render_template('game.html')

@app.route('/share', methods=['POST', 'GET'])
@login_required
def share():
    # get the total score of all users and sort by total score
    user_score=db.session.query(ScoreModel.user_id,func.sum(ScoreModel.score)).group_by(ScoreModel.user_id).order_by(func.sum(ScoreModel.score).desc()).all()
    user_rank=0 #current user's rank
    total_score=0 #current user's total score
    if user_score is not None:
        for user in user_score:
            user_rank+=1
            if user.user_id==current_user.id:
                total_score=user[1]
                break
        return {'user_id':current_user.id, 'username':current_user.name, 'ranking':user_rank, 'score':total_score}
    return render_template('share.html')

# ---------------------admin controller-----------------------------------------------------------------------------------------------------------------------------------------------------------
@app.route('/admin_question_list', methods=['POST', 'GET'])
# get all question data for admin (id, content, answer)
def get_questions():
    questions = QuestionModel.query.all()
    result=[]
    if questions is not None:
        for question in questions:
            result.append({'id': question.id, 'content': question.content, 'answer': question.answer})
        return {'question_list': result}
    return {'status': 'fail'}

@app.route('/admin_search_keyword', methods=['POST', 'GET'])
# search question by keywords in question content
def search_by_keywords():
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        questions = QuestionModel.query.filter(QuestionModel.content.like('%'+keyword+'%')).all()
        result=[]#result list will be empty if cannot find the keyword in all question content
        if questions is not None:
            for question in questions:
                result.append({'id': question.id, 'content': question.content, 'answer': question.answer})
            return {'question_list': result}
        return {'status': 'fail'}
    return render_template('admin_index.html')

@app.route('/admin_get_question/<int:question_id>', methods=['POST', 'GET'])
# get a question by question id
def get_question_by_id(question_id):
    question = QuestionModel.query.filter_by(id=question_id).first()
    if question is not None:
        return {'content': question.content, 'answer': question.answer}
    return {'status': 'fail'}

@app.route('/admin_delete_question/<int:question_id>', methods=['POST', 'GET'])
# delete a question by question id
def delete_question(question_id):
    question = QuestionModel.query.filter_by(id=question_id).first()
    if question is not None:
        db.session.delete(question)
        try:
            db.session.commit()
        except Exception as e:
            raise e
        return {'status':'success'}
    return {'status': 'fail'}

@app.route('/admin_add_question', methods=['POST', 'GET'])
# add a new question
def add_question():
    if request.method == 'POST':
        content = request.form.get('content')
        answer = request.form.get('answer')
        question = QuestionModel(content=content, answer=answer)
        db.session.add(question)
        try:
            db.session.commit()
        except Exception as e:
            raise e
        return {'status':'success'}
    return render_template('game.html')

@app.route('/admin_edit_question/<int:question_id>', methods=['POST', 'GET'])
# edit a question by question id
def edit_question(question_id):
    if request.method == 'POST':
        question = QuestionModel.query.filter_by(id=question_id).first()
        question.content = request.form.get('content')
        question.answer = request.form.get('answer')
        try:
            db.session.commit()
        except Exception as e:
            raise e
        return {'status':'success'}
    return render_template('game.html')
