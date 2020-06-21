"""App factory file."""

import firebase_admin
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

from .config import config

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
firebase = firebase_admin.initialize_app()


def create_app(config_name):
    """Application factory."""
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    app.config.from_object(config[config_name])
    initialize_extensions(app)
    register_blueprints(app)
    return app


def initialize_extensions(app):
    db.init_app(app)
    flask_bcrypt.init_app(app)


def register_blueprints(app):
    from sme_financing.main.api_v1 import blueprint as api_v1

    app.register_blueprint(api_v1)
