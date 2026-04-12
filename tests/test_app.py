import pytest
import sqlite3
import os
import tempfile
import app as flask_app

@pytest.fixture
def client():
    # Create a temporary file for the database
    db_fd, db_path = tempfile.mkstemp()
    
    # Override the DB_FILE to use the temp database
    flask_app.DB_FILE = db_path
    
    flask_app.app.config['TESTING'] = True

    # Initialize the database
    flask_app.init_db()

    with flask_app.app.test_client() as client:
        yield client

    # Cleanup the temp database after tests finish
    os.close(db_fd)
    os.unlink(db_path)


def test_home_page(client):
    """Test that the home page loads successfully"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'EventHive' in rv.data


def test_register_and_login(client):
    """Test registering a new user and logging in"""
    # Register
    rv = client.post('/register', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    
    assert b'Registration successful' in rv.data
    assert rv.status_code == 200

    # Login
    rv_login = client.post('/login', data=dict(
        username='testuser',
        password='testpassword'
    ), follow_redirects=True)
    
    assert b'Logged in successfully' in rv_login.data
    # Verify we are on dashboard
    assert b'dashboard' in rv_login.data.lower()
