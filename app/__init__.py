from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db=SQLAlchemy()
login_manager=LoginManager()

basedir=os.path.abspath(os.path.dirname(__file__))
def create_app():
    app=Flask(__name__,instance_relative_config=True)
    app.config.from_object("app.config")
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view="auth.login"
    from . import models
    from app.models import User
    #load users
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    #blue prints of rpages
    from app.auth import auth_bp
    from app.main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)


    with app.app_context():
        db.create_all()
    
    print(app.url_map)
    return app

