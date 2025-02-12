import unittest
from app import app, db
from models import User

class FlaskTestCase(unittest.TestCase):
    # ✅ Set up test environment before each test
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # ✅ Create a new database for testing
        with app.app_context():
            db.create_all()

    # ✅ Test if the Flask app is running
    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    # ✅ Test database connection
    def test_database_connection(self):
        with app.app_context():
            result = db.session.execute("SELECT 1").fetchone()
            self.assertIsNotNone(result)

    # ✅ Test user registration
    def test_register(self):
        response = self.app.post('/register', data=dict(
            username="testuser",
            password="Test@1234",
            confirm_password="Test@1234"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome, our new apprentice!", response.data)

    # ✅ Test user login
    def test_login(self):
        # Create a test user
        with app.app_context():
            user = User(username="testuser")
            user.set_password("Test@1234")
            db.session.add(user)
            db.session.commit()

        response = self.app.post('/login', data=dict(
            username="testuser",
            password="Test@1234"
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome back, our bartender apprentice!", response.data)

    # ✅ Test logout functionality
    def test_logout(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"You have been logged out.", response.data)

    # ✅ Clean up database after each test
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()