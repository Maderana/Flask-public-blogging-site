import unittest
from app import create_app, db

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register(self):
        response = self.client.post('/register', data={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        self.client.post('/register', data={'username': 'testuser', 'password': 'testpass'})
        response = self.client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        self.client.post('/register', data={'username': 'testuser', 'password': 'testpass'})
        self.client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)