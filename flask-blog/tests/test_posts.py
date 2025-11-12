import unittest
from app import create_app, db
from app.models import User, Post

class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            user = User(username='testuser', password='testpass')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        with self.client:
            self.client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
            response = self.client.post('/new_post', data={'title': 'Test Post', 'content': 'This is a test.'})
            self.assertEqual(response.status_code, 302)

    def test_post_detail(self):
        with self.client:
            self.client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
            self.client.post('/new_post', data={'title': 'Test Post', 'content': 'This is a test.'})
            response = self.client.get('/post/1')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Post', response.data)