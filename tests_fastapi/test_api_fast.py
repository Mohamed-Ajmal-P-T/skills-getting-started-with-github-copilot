from fastapi.testclient import TestClient
import pytest

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    # Keep tests isolated by resetting the in-memory store each run
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
    })


client = TestClient(app)


def test_get_activities_fastapi():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["max_participants"] == 12


def test_signup_for_activity_fastapi():
    resp = client.post("/activities/Chess Club/signup?email=testuser@mergington.edu")
    assert resp.status_code == 200
    json_data = resp.json()
    assert "Signed up testuser@mergington.edu" in json_data["message"]
    assert "testuser@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_nonexistent_activity_fastapi():
    resp = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert resp.status_code == 404


def test_unregister_from_activity_fastapi():
    resp = client.post("/activities/Chess Club/unregister?email=michael@mergington.edu")
    assert resp.status_code == 200
    assert "Unregistered michael@mergington.edu" in resp.json()["message"]
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_nonexistent_participant_fastapi():
    resp = client.post("/activities/Chess Club/unregister?email=notfound@mergington.edu")
    assert resp.status_code == 404
