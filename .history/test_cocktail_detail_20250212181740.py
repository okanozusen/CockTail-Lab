import unittest
from app import app, db
from models import User, Cocktail
from flask_login import login_user


class CocktailDetailTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()
            user = User(username="testuser", password_hash="hashedpassword")
            db.session.add(user)
            db.session.commit()
            self.test_user = user

            cocktail = Cocktail(
                name="Test Cocktail",
                cup="Martini Glass",
                capacity=8,
                ingredients=[{"name": "Vodka", "ounces": 2}, {"name": "Lime Juice", "ounces": 1}],
                color="#FFD700",
                sweetness=5,
                bitterness=3,
                smoothness=7,
                strength=6,
                freshness=4,
                enjoyment_rating=8,
                final_strength=7,
                user_id=self.test_user.id
            )
            db.session.add(cocktail)
            db.session.commit()
            self.test_cocktail = cocktail

    def tearDown(self):
        """Tear down the database"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_access_cocktail_detail(self):
        """Test if users can view cocktail details"""
        with self.client:
            self.client.post('/login', data={'username': 'testuser', 'password': 'password'})
            response = self.client.get(f'/cocktail_detail/{self.test_cocktail.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Cocktail', response.data)

    def test_unauthorized_cocktail_access(self):
        """Test that unauthorized users cannot access another user's cocktail"""
        with self.client:
            response = self.client.get(f'/cocktail_detail/{self.test_cocktail.id}')
            self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_delete_cocktail(self):
        """Test if a user can delete their cocktail"""
        with self.client:
            self.client.post('/login', data={'username': 'testuser', 'password': 'password'})
            response = self.client.post(f'/delete_cocktail/{self.test_cocktail.id}')
            self.assertEqual(response.status_code, 200)

            # Verify cocktail was deleted
            with app.app_context():
                deleted_cocktail = Cocktail.query.get(self.test_cocktail.id)
                self.assertIsNone(deleted_cocktail)


if __name__ == '__main__':
    unittest.main()
