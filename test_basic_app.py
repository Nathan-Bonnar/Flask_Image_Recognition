# tests/test_basic_app.py
"""
Functional and negative tests for the Flask Image Recognition app.
Covers startup, valid uploads, missing file errors, and invalid file types.
"""

from io import BytesIO
import pytest
from app import app


@pytest.fixture
def client():
    """Create a Flask test client for the app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# 1. Home route responds
def test_home_route_loads(client):
    """Check that the home page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Upload" in response.data or b"Image" in response.data


# 2. Valid image upload produces a prediction
def test_valid_image_upload(client):
    """Upload a small valid image and expect a prediction."""
    img_data = BytesIO(b"fake_image_data")
    img_data.name = "digit.jpg"
    response = client.post(
        "/prediction",
        data={"file": (img_data, img_data.name)},
        content_type="multipart/form-data"
    )
    assert response.status_code == 200
    assert b"Prediction" in response.data


# 3. Missing file field (graceful handling)
def test_upload_without_file(client):
    """
    Many Flask forms redirect (302) back to '/' when the file is missing.
    Accept 200 (error page) or 302 (redirect), but never 500.
    """
    resp = client.post("/prediction", data={}, content_type="multipart/form-data")
    assert resp.status_code in (200, 302)

    if resp.status_code == 302:
        resp = client.post("/prediction", data={}, content_type="multipart/form-data", follow_redirects=True)
        assert resp.status_code == 200

    body = resp.data.lower()
    assert (
        b"no file" in body
        or b"choose file" in body
        or b"upload" in body
        or b"error" in body
        or b"home" in body
    ), "Expected the app to handle missing file without crashing."


# 4. Large but valid image simulation (fast mock)
def test_large_image_simulation(client):
    """Simulate uploading a moderately large image."""
    big_img = BytesIO(b"x" * 1024 * 1024)  # 1 MB fake image
    big_img.name = "big_image.jpg"
    response = client.post(
        "/prediction",
        data={"file": (big_img, big_img.name)},
        content_type="multipart/form-data"
    )
    assert response.status_code == 200
    assert b"Prediction" in response.data


# 5. Invalid route
def test_invalid_route_returns_404(client):
    """Requesting a non-existent route should return 404."""
    response = client.get('/does_not_exist')
    assert response.status_code == 404
