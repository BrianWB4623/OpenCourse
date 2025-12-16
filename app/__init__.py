from flask import Flask, render_template
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
    #blue prints of rpages
    from app.auth import auth_bp
    from app.main import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)


    with app.app_context():
        db.create_all()
        try:
            from sqlalchemy import text
            # add column to assignment if it doesn't exist
            try:
                db.session.execute(text('ALTER TABLE assignment ADD COLUMN course_id INTEGER'))
                db.session.commit()
            except Exception:
                db.session.rollback()
            # add column to course_material if missing
            try:
                db.session.execute(text('ALTER TABLE course_material ADD COLUMN course_id INTEGER'))
                db.session.commit()
            except Exception:
                db.session.rollback()
        except Exception:
            pass
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500
    
    print(app.url_map)
    return app

