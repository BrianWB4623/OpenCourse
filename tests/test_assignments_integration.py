# tests/test_integration_assignments.py
from app import db
from app.models import Assignment

def login(client, username, password):
    return client.post(
        "/auth/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )

def test_assignment_create_authorized(client, instructor_user):
    login(client, instructor_user.username, "testpassword")
    response = client.post(
        "/assignments/create",
        data={"title": "Test HW", "description": "Assignment details"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Test HW" in response.data

def test_assignment_create_unauthorized(client):
    """Anonymous users should be redirected."""
    response = client.post(
        "/assignments/create",
        data={"title": "Hack HW"},
        follow_redirects=False,
    )
    assert response.status_code in (302, 401)

def test_assignment_delete_authorized(client, instructor_user, app):
    login(client, instructor_user.username, "testpassword")

    with app.app_context():
        hw = Assignment(title="Delete Me", instructor_id=instructor_user.id)
        db.session.add(hw)
        db.session.commit()
        hw_id = hw.id

    response = client.post(f"/assignments/{hw_id}/delete", follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        assert Assignment.query.get(hw_id) is None
