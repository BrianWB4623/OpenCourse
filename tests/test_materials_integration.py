# tests/test_integration_materials.py
from app import db
from app.models import CourseMaterial

def login(client, username, password):
    return client.post(
        "/auth/login",
        data={"username": username, "password": password},
        follow_redirects=True,
    )

def test_material_create_authorized(client, instructor_user):
    login(client, instructor_user.username, "testpassword")
    response = client.post(
        "/materials/create",
        data={"title": "Lecture 1", "description": "Intro slides"},
        follow_redirects=True,
    )
    assert b"Lecture 1" in response.data

def test_material_create_unauthorized(client):
    response = client.post(
        "/materials/create",
        data={"title": "Hack Material"},
        follow_redirects=False,
    )
    assert response.status_code in (302, 401)

def test_material_list_loads(client):
    response = client.get("/materials")
    assert response.status_code == 200
    assert b"Materials" in response.data
