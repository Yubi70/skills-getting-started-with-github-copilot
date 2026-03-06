"""
Tests for the Mergington High School Activities API
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to a clean state before each test"""
    original_participants = {name: list(data["participants"]) for name, data in activities.items()}
    yield
    for name, data in activities.items():
        data["participants"] = original_participants[name]


client = TestClient(app)


def test_get_activities():
    """Test that the activities endpoint returns all activities"""
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 9
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert "Basketball Team" in data
    assert "Swimming Club" in data
    assert "Art Studio" in data
    assert "Drama Club" in data
    assert "Debate Team" in data
    assert "Science Club" in data


def test_signup_for_activity():
    """Test that a student can sign up for an activity"""
    # Arrange
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_signup_for_nonexistent_activity():
    """Test that signing up for a nonexistent activity returns 404"""
    # Arrange
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/NonExistentActivity/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_duplicate_prevention():
    """Test that a student cannot sign up for the same activity twice"""
    # Arrange
    email = "michael@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()


def test_unregister_from_activity():
    """Test that a student can unregister from an activity"""
    # Arrange
    email = "michael@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]


def test_unregister_not_signed_up():
    """Test that unregistering a student who is not signed up returns 400"""
    # Arrange
    email = "notregistered@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"].lower()


def test_unregister_from_nonexistent_activity():
    """Test that unregistering from a nonexistent activity returns 404"""
    # Act
    response = client.delete("/activities/NonExistentActivity/signup?email=student@mergington.edu")

    # Assert
    assert response.status_code == 404
