import unittest
from app import app, db
from flask_login import login_user
from models import User, Cocktail

class CreateCocktailTestCase(unittest.TestCase):
    # ✅ Setup test client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # ✅ Create test database session
        with app.app_context():
            db.create_all()
            self.test_user = User(username="testuser", password_hash="hashedpassword")
            db.session.add(self.test_user)
            db.session.commit()

    # ✅ Test cocktail creation requires authentication
    def test_create_cocktail_unauthenticated(self):
        """
        # Test: Ensure unauthenticated users cannot access the create cocktail page.
        - Expected Behavior: Redirect to login page.
        """
        response = self.app.get('/create_cocktail', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)  # Redirects to login page

    # ✅ Test cocktail creation when logged in
    def test_create_cocktail_authenticated(self):
        """
        # Test: Ensure authenticated users can create a cocktail.
        - Expected Behavior: Cocktail should be created successfully and appear in the response.
        """
        with self.app.session_transaction() as sess:
            sess['_user_id'] = self.test_user.id  # Simulating login

        response = self.app.post('/create_cocktail', json={
            "name": "Test Cocktail",
            "cup": "Martini Glass",
            "capacity": 8,
            "ingredients": [{"name": "Vodka", "ounces": 2}],
            "color": "#D1D1D1",
            "sweetness": 3,
            "bitterness": 5,
            "strength": 7,
            "freshness": 2
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Cocktail", response.data)  # Cocktail appears in response

    # ✅ Cleanup after tests
    def tearDown(self):
        """
        # Cleanup: Remove test user and cocktails after the test runs.
        """
        with app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == '__main__':
    unittest.main()
