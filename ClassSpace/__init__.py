import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_cors import CORS
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    db.init_app(app)
    cors.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # migrate.init_app(app, db)
    with app.app_context():
        from . import auth
        app.register_blueprint(auth.bp)

        from . import dashboard
        app.register_blueprint(dashboard.bp)
        app.add_url_rule('/dashboard', endpoint='dashboard')

        db.create_all()

        return app
