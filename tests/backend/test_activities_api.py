from src import app as app_module


def test_list_activities_empty(client):
    # Arrange
    app_module.activities.clear()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {}


def test_create_and_get_activity(client):
    # Arrange
    app_module.activities["cycling"] = {"participants": []}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert "cycling" in response.json()


def test_signup_and_remove_sequence(client):
    # Arrange
    app_module.activities["yoga"] = {"participants": []}

    # Act
    signup = client.post("/activities/yoga/signup", params={"email": "bob@example.com"})

    # Assert signup
    assert signup.status_code == 200
    assert "bob@example.com" in app_module.activities["yoga"]["participants"]

    # Act (removal)
    removal = client.delete(
        "/activities/yoga/participants", params={"email": "bob@example.com"}
    )

    # Assert removal
    assert removal.status_code == 200
    assert app_module.activities["yoga"]["participants"] == []


def test_signup_nonexistent_activity(client):
    # Arrange
    app_module.activities.clear()

    # Act
    response = client.post("/activities/nonexistent/signup", params={"email": "nobody@example.com"})

    # Assert
    assert response.status_code == 404
