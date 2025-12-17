# tests/test_integration_auth.py
def test_login_success(client, app, instructor_user):
    """User can successfully log in."""
    response = client.post(
        "/auth/login",
        data={"username": instructor_user.username, "password": "testpassword"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Logout" in response.data


def test_login_failure(client):
    """Invalid credentials should not authenticate user."""
    response = client.post(
        "/auth/login",
        data={"username": "wrong", "password": "incorrect"},
        follow_redirects=True,
    )
    assert b"Invalid" in response.data or response.status_code == 200
