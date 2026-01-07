import pytest

import requests

@pytest.fixture(autouse=True)
def reset_activities():
    # Assumes the app is running locally for test isolation
    try:
        requests.post("http://localhost:8000/test/reset-activities")
    except Exception:
        pass
import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Basketball Team"
    # Remove if already present
    client.delete(f"/activities/{activity}/participants/{email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    # Clean up
    client.delete(f"/activities/{activity}/participants/{email}")

def test_remove_participant():
    email = "removeuser@mergington.edu"
    activity = "Tennis Club"
    # Ensure user is not present
    client.delete(f"/activities/{activity}/participants/{email}")
    # Sign up the user
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200
    # Now remove
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]
    # Removing again should 404
    response2 = client.delete(f"/activities/{activity}/participants/{email}")
    assert response2.status_code == 404
