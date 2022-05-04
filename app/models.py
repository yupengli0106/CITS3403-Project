from config import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#Get the user object and store it in the session
@login_manager.user_loader
def load_user(user_id):
    return UserModel.query.get(int(user_id))

# user model
class UserModel(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    hash_password = db.Column(db.String(200), nullable=False)

    # convert password to hash value
    def encode_password(password):
        #hash value of password
        hash_password = generate_password_hash(password)
        return hash_password

    # Verify if the hash value of password is equal to the input password
    def decode_password(hash_password, password):
        check_password = check_password_hash(hash_password, password)
        return check_password #True or False

# question model
class QuestionModel(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text,nullable=False)
    answer = db.Column(db.String(4), nullable=False)

class FileReader():
    # read QA.txt file and store questions in database
    def read_file(db,filename):
        with open(filename, 'r') as f:
            content = f.readlines()
        for line in content:
            line = line.strip()
            line = line.split('\t')
            question = QuestionModel(id=[0], answer=line[1], content=line[2])
            db.session.add(question)
        try:
            db.session.commit()
        except:
            print("---Duplicate Database Created---")

