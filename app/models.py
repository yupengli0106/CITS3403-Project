from app import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#Get the user object and store as current_user through flask_login
@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

# User Data
class UserModel(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    hash_password = db.Column(db.String(200), nullable=False)
    admin = db.Column(db.Boolean, default=False)

     # convert password to hash value
    def encode_password(self, password):
        self.hash_password = generate_password_hash(password)

    # Verify if the hash value of password is equal to the input password
    def decode_password(self, password):
        return check_password_hash(self.hash_password, password) #return True or False

# Question Data
class QuestionModel(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text,nullable=False)
    answer = db.Column(db.String(4), nullable=False)

# Score Data
class ScoreModel(db.Model):
    __tablename__ = 'scores'
    user_id = db.Column(db.Integer,  primary_key=True, nullable=False)
    ques_id = db.Column(db.Integer,  primary_key=True, nullable=False)
    socre = db.Column(db.Integer, nullable=False)

# initialize the database
class FileReader():
    # read QA.txt file and store questions in database
    def read_file(db,filename):
        # Prevent duplicate data generation
        QuestionModel.query.delete()
        with open(filename, 'r') as f:
            content = f.readlines()
        for line in content:
            line = line.strip()
            line = line.split('\t')
            question = QuestionModel(answer=line[0], content=line[1])
            db.session.add(question)
        try:
            db.session.commit()
        except Exception as e:
            raise e

