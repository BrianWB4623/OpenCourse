#test_routes.py
from flask import url_for


def test_assignments_list_route_loads(app, client, instructor_user):
    """The assignments list route returns HTTP 200 when logged in."""
    # log in first
    client.post("/auth/login", data={"username": "Professor Rojas", "password": "testpassword"})
    response = client.get("/assignments")
    assert response.status_code == 200
    assert b"html" in response.data or response.mimetype == "text/html"


def test_materials_list_route_loads(app, client, instructor_user):
    """The materials list route returns HTTP 200 when logged in."""
    client.post("/auth/login", data={"username": "Professor Rojas", "password": "testpassword"})
    response = client.get("/materials")
    assert response.status_code == 200
    assert response.mimetype == "text/html"


def test_create_assignment_requires_login(app, client):
    """Protected route should redirect anonymous users to login."""
    response = client.get("/assignments/create")
    # login_required should redirect to login view
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_create_assignment_accessible_after_login(app, client, instructor_user):
    """Logged-in instructor can load the assignment creation page."""
    # Log the user in via the real login route
    login_response = client.post(
        "/auth/login",
        data={
            "username": "Professor Rojas",
            "password": "testpassword",
            "remember_me": False,
        },
        follow_redirects=True,
    )
    assert login_response.status_code == 200

    # Now access protected route
    response = client.get("/assignments/create")
    assert response.status_code == 200


def test_student_sees_view_submission_button(app, client, instructor_user, student_user):
    """When a student has submitted, the assignment detail shows a View button."""
    with app.app_context():
        from app.models import Assignment, Submission, User
        from app import db as _db

        # fetch fresh instances (avoid detached fixture objects)
        inst = User.query.filter_by(username="Professor Rojas").first()
        stud = User.query.filter_by(username="student1").first()

        # create an assignment
        a = Assignment(title="Test Assignment", description="Do something", instructor_id=inst.id)
        _db.session.add(a)
        _db.session.commit()

        # create a submission for the student
        s = Submission(assignment_id=a.id, student_id=stud.id, content="My answer")
        _db.session.add(s)
        _db.session.commit()
        a_id = a.id

    # log in as student
    login_response = client.post(
        "/auth/login",
        data={"username": "student1", "password": "testpassword"},
        follow_redirects=True,
    )
    assert login_response.status_code == 200

    # load the assignment detail page
    response = client.get(f"/assignments/{a_id}")
    assert response.status_code == 200
    # debug: ensure submission exists and is owned by student1
    with app.app_context():
        from app.models import Submission, User
        sub = Submission.query.filter_by(assignment_id=a_id).first()
        u = User.query.filter_by(username="student1").first()
        assert sub is not None
        assert u is not None
        assert sub.student_id == u.id

    assert b"View your Submission" in response.data