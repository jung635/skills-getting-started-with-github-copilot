import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_unregister():
    activity = "Basketball Team"
    email = "testuser@mergington.edu"
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert "message" in response.json()
    # Duplicate signup should fail
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    # Unregister
    response_del = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response_del.status_code == 200
    assert "message" in response_del.json()
    # Unregister again should fail
    response_del2 = client.delete(f"/activities/{activity}/signup?email={email}")
    assert response_del2.status_code == 404

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404

def test_unregister_nonexistent_activity():
    response = client.delete("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
