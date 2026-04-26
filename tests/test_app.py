import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_root_redirect(client):
    # Arrange - client fixture provides TestClient
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code == 200
    assert "Mergington High School" in response.text


def test_get_activities(client):
    # Arrange - client fixture provides TestClient
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "schedule" in data["Chess Club"]
    assert "max_participants" in data["Chess Club"]
    assert "participants" in data["Chess Club"]


def test_signup_success(client):
    # Arrange - client fixture and test data
    activity_name = "Basketball Team"  # Has empty participants
    email = "test@example.com"
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity_name}" in response.json()["message"]


def test_signup_duplicate(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "test@example.com"
    # Act - first signup
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Act - duplicate signup
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "Student already signed up" in str(response.json())


def test_signup_invalid_activity(client):
    # Arrange
    email = "test@example.com"
    # Act
    response = client.post("/activities/Invalid Activity/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in str(response.json())


def test_unregister_success(client):
    # Arrange
    activity_name = "Soccer Club"  # Empty initially
    email = "test@example.com"
    # Act - signup first
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Act - unregister
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Unregistered {email} from {activity_name}" in response.json()["message"]


def test_unregister_not_signed_up(client):
    # Arrange
    activity_name = "Soccer Club"
    email = "test@example.com"
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert "Student not signed up for this activity" in str(response.json())


def test_unregister_invalid_activity(client):
    # Arrange
    email = "test@example.com"
    # Act
    response = client.delete("/activities/Invalid Activity/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in str(response.json())