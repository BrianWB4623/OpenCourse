# tests/test_models_expanded.py
from app import db
from app.models import User, Assignment, CourseMaterial

def test_user_role_defaults(app):
    with app.app_context():
        u = User(username="sam", email="sam@example.com", password_hash="pw")
        db.session.add(u)
        db.session.commit()
        assert u.role in ("student", None, "")
