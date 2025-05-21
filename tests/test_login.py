import unittest
from flask_login import current_user
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

class TestLoginFunction(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database

        # Create test client
        self.client = app.test_client()

        # Create application context
        self.app_context = app.app_context()
        self.app_context.push()

        # Create database tables
        db.create_all()

        # Create test users
        test_user1 = User(
            name='Harsh',
            email='harsh@example.com',
            password=generate_password_hash('password@123')
        )
        
        test_user2 = User(
            name='Test User',
            email='test@example.com',
            password=generate_password_hash('password123')
        )
        
        db.session.add(test_user1)
        db.session.add(test_user2)
        db.session.commit()

    def tearDown(self):
        """Clean up after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_page_loads(self):
        """Test that login page loads correctly"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_successful_login(self):
        """Test successful login with valid credentials"""
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123',
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(current_user.is_authenticated)
        self.assertEqual(current_user.email, 'test@example.com')
        self.assertIn(b'Login successful', response.data)

    def test_login_with_invalid_email(self):
        """Test login with invalid email"""
        response = self.client.post('/login', data={
            'email': 'nonexistent@example.com',
            'password': 'password123',
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(current_user.is_authenticated)
        self.assertIn(b'Invalid email or password', response.data)

    def test_login_with_invalid_password(self):
        """Test login with invalid password"""
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword',
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(current_user.is_authenticated)
        self.assertIn(b'Invalid email or password', response.data)

    def test_login_with_empty_credentials(self):
        """Test login with empty credentials"""
        response = self.client.post('/login', data={
            'email': '',
            'password': '',
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(current_user.is_authenticated)
        # WTForms validation should catch this
        self.assertIn(b'This field is required', response.data)

    def test_redirect_when_already_logged_in(self):
        """Test redirect when user is already logged in"""
        # First login
        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123',
        }, follow_redirects=True)

        # Try to access login page again
        response = self.client.get('/login', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        # Should be redirected to index page
        self.assertIn(b'Urban Climate Risk Predictor', response.data)

    def test_redirect_to_next_page(self):
        """Test redirect to 'next' page after login"""
        # Try to access a protected page
        self.client.get('/logout')  # Make sure we're logged out

        # Simulate accessing a protected page that redirects to login
        response = self.client.get('/logout', follow_redirects=True)

        # Now login with the next parameter
        response = self.client.post('/login?next=%2Flogout', data={
            'email': 'test@example.com',
            'password': 'password123',
        }, follow_redirects=True)

        # Should be redirected to the logout page and then back to index
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Urban Climate Risk Predictor', response.data)

if __name__ == '__main__':
    unittest.main()