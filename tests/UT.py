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
    q1 = QuestionModel(content='question1', answer='1')
    q2 = QuestionModel(content='question2', answer='2')


    db.session.add_all([s1, s2, q1, q2])
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

  def test_get_all_questions(self):
    response = self.client.get('/admin_question_list')
    json_data = json.loads(response.data)
    self.assertIn('question_list', json_data)
    self.assertEqual(json_data['question_list'], [{'id':1,'content': 'question1', 'answer': '1'}, {'id':2,'content': 'question2', 'answer': '2'}])

  def test_search_by_keywords(self):
    response = self.client.get('/admin_question_list?keywords=question')
    json_data = json.loads(response.data)
    self.assertIn('question_list', json_data)
    self.assertEqual(json_data['question_list'], [{'id':1,'content': 'question1', 'answer': '1'}, {'id':2,'content': 'question2', 'answer': '2'}])

  def test_get_question_by_id(self):
    response = self.client.get('/admin_get_question/1')
    json_data = json.loads(response.data)
    self.assertEqual(json_data['content'], 'question1')
    self.assertEqual(json_data['answer'], '1')

  def test_delete_question_by_id(self):
    response = self.client.post('/admin_delete_question/2')
    json_data = json.loads(response.data)
    self.assertEqual(json_data['status'], 'success')

    response = self.client.get('/admin_delete_question/3')
    json_data = json.loads(response.data)
    self.assertEqual(json_data['status'], 'fail')

  def test_add_question(self):
    response = self.client.post('/admin_add_question', data=dict(content='question3', answer='3'))
    json_data = json.loads(response.data)
    self.assertEqual(json_data['status'], 'success')

    q3 = QuestionModel.query.filter_by(content='question3').first()
    self.assertEqual(q3.content, 'question3')
    self.assertEqual(q3.answer, '3')

  def test_edit_question(self):
    response = self.client.post('/admin_edit_question/1', data=dict(content='question1_edited', answer='1_edited'))
    json_data = json.loads(response.data)
    self.assertEqual(json_data['status'], 'success')

    q1 = QuestionModel.query.filter_by(id=1).first()
    self.assertEqual(q1.content, 'question1_edited')
    self.assertEqual(q1.answer, '1_edited')



if __name__=='__main__':
  unittest.main(verbosity=2)
