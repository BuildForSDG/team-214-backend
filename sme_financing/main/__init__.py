"""App factory file."""

# from werkzeug.contrib.fixers import ProxyFix
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from .config import config

db = SQLAlchemy()
flask_bcrypt = Bcrypt()


def create_app(config_name):
    """Application factory."""
    app = Flask(__name__)
    # app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config.from_object(config[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)
    return app
