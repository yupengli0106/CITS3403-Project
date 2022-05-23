import json
import unittest, os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.models import UserModel, QuestionModel, ScoreModel
from app import app, db 

class UserModelCase(unittest.TestCase):
  def setUp(self):
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'test.db')
    app.testing=True
    # virtual test environment
    self.client = app.test_client()

    db.create_all()

    s1 = UserModel(username='test')
    s1.encode_password('test')
    s2 = UserModel(username='admin', admin=True)
    s2.encode_password('admin')

    db.session.add_all([s1, s2])
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def test_user_registration(self):
    response = self.client.post('/register', data=dict(username='test3', password='test'))
    json_data = json.loads(response.data)
    self.assertIn('status', json_data)
    self.assertEqual(json_data['status'], 'success')

    response = self.client.post('/register', data=dict(username='test3', password='test'))
    json_data = json.loads(response.data)
    self.assertIn('status', json_data)
    self.assertEqual(json_data['status'], 'fail')

  def test_user_login(self):
    response = self.client.post('/login', data=dict(username='test', password='test'))
    json_data = json.loads(response.data)
    self.assertIn('status', json_data)
    self.assertEqual(json_data['status'], 'success')
    
    response = self.client.post('/login', data=dict(username='111', password='111'))
    json_data = json.loads(response.data)
    self.assertIn('status', json_data)
    self.assertEqual(json_data['status'], 'fail')

  def test_password_hashing(self):
    s = UserModel.query.filter_by(username='test').first()
    s.encode_password('test')
    self.assertFalse(s.decode_password('case'))
    self.assertTrue(s.decode_password('test'))

  def test_admin_login(self):
    response = self.client.post('/admin_login', data=dict(username='admin', password='admin', admin=True))
    json_data = json.loads(response.data)
    self.assertIn('status', json_data)
    self.assertEqual(json_data['status'], 'success')

    response = self.client.post('/admin_login', data=dict(username='admin', password='test'))
    json_data = json.loads(response.data)
    self.assertIn('status', json_data)
    self.assertEqual(json_data['status'], 'fail')



if __name__=='__main__':
  unittest.main(verbosity=2)
