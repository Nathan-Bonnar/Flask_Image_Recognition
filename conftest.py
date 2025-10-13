"""Conftest imports the flask app for testing"""

import pytest
from app import app  # This imports the Flask app for testing

@pytest.fixture
def client():
    """Import the client app for testing"""
    with app.test_client() as client:
        yield client
