from src import app as app_module


def test_root_redirect(client):
    # Arrange
    # no setup required for root redirect

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_empty(client):
    # Arrange
    app_module.activities.clear()

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json() == {}


def test_signup_success(client):
    # Arrange
    app_module.activities["hiking"] = {"participants": []}

    # Act
    response = client.post(
        "/activities/hiking/signup", params={"email": "alice@example.com"}
    )

    # Assert
    assert response.status_code == 200
    assert "Signed up alice@example.com for hiking" in response.json().get("message", "")

def test_signup_duplicate(client):
    # Arrange
    app_module.activities["hiking"] = {"participants": ["alice@example.com"]}

    # Act
    response = client.post(
        "/activities/hiking/signup", params={"email": "alice@example.com"}
    )

    # Assert
    assert response.status_code == 400

def test_signup_invalid(client):
    # Arrange
    app_module.activities["hiking"] = {"participants": []}

    # Act
    response = client.post("/activities/hiking/signup", params={})

    # Assert
    assert response.status_code == 422

def test_remove_participant_success(client):
    # Arrange
    app_module.activities["hiking"] = {"participants": ["alice@example.com"]}

    # Act
    response = client.delete(
        "/activities/hiking/participants", params={"email": "alice@example.com"}
    )

    # Assert
    assert response.status_code == 200
    assert "Removed alice@example.com from hiking" in response.json().get("message", "")

def test_remove_not_signed_up(client):
    # Arrange
    app_module.activities["hiking"] = {"participants": []}

    # Act
    response = client.delete(
        "/activities/hiking/participants", params={"email": "alice@example.com"}
    )

    # Assert
    assert response.status_code == 404

def test_remove_nonexistent_activity(client):
    # Arrange
    # no setup – activity does not exist

    # Act
    response = client.delete(
        "/activities/nonexistent/participants", params={"email": "alice@example.com"}
    )

    # Assert
    assert response.status_code == 404
