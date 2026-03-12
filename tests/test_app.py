import copy
from fastapi.testclient import TestClient
import src.app as appmod

ORIGINAL_ACTIVITIES = copy.deepcopy(appmod.activities)

import pytest

@pytest.fixture(autouse=True)
def client():
    # Arrange: reset in-memory activities before each test
    appmod.activities.clear()
    appmod.activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    with TestClient(appmod.app) as c:
        yield c


def test_get_activities(client):
    # Arrange: (nothing to set up)
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_success(client):
    # Arrange
    email = "test@mergington.edu"
    activity = "Chess Club"

    # Act
    resp = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert resp.status_code == 200
    assert f"Signed up {email}" in resp.json()["message"]
    data = client.get("/activities").json()
    assert email.lower() in [p.lower() for p in data[activity]["participants"]]


def test_signup_normalization_and_duplicate(client):
    # Arrange
    raw_email = " NewUser@Mergington.EDU "
    normalized = "newuser@mergington.edu"
    activity = "Chess Club"

    # Act
    resp = client.post(f"/activities/{activity}/signup?email={raw_email}")

    # Assert
    assert resp.status_code == 200

    # Act: try signing up again with normalized email
    resp2 = client.post(f"/activities/{activity}/signup?email={normalized}")

    # Assert
    assert resp2.status_code == 400


def test_signup_duplicate_existing(client):
    # Arrange
    existing = appmod.activities["Chess Club"]["participants"][0]
    activity = "Chess Club"

    # Act
    resp = client.post(f"/activities/{activity}/signup?email={existing}")

    # Assert
    assert resp.status_code == 400


def test_unregister_success(client):
    # Arrange
    existing = appmod.activities["Chess Club"]["participants"][0]
    activity = "Chess Club"

    # Act
    resp = client.post(f"/activities/{activity}/unregister?email={existing}")

    # Assert
    assert resp.status_code == 200
    data = client.get("/activities").json()
    assert all(existing.lower() != p.lower() for p in data[activity]["participants"])


def test_unregister_not_signed_up(client):
    # Arrange
    activity = "Chess Club"
    email = "not@here"

    # Act
    resp = client.post(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert resp.status_code == 400
