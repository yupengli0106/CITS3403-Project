from app import app, db

from app.models import FileReader, UserModel


if __name__ == '__main__':
    # initialize questions
    FileReader.read_file(db, 'app/static/QA.txt')
    # initialize admin account
    admin = UserModel(username='admin', admin=True)
    admin.encode_password('admin')
    db.session.add(admin)
    try:
        db.session.commit()
    except:
        db.session.rollback()

    app.run()
