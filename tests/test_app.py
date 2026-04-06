import pytest
from app import create_app
from app.database import db

@pytest.fixture
def client():
    # Setup test app
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use in-memory DB for tests

    with app.app_context():
        # recreate models
        db.create_all()

    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test that the index route returns successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b"EventHive" in response.data
