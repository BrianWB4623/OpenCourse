import os
basedir=os.path.abspath(os.path.dirname(__file__))
SECRET_KEY='will-replace-later'
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False
