import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

env_path = os.path.join(basedir, '../../.env')
load_dotenv(dotenv_path=env_path)
print(env_path)

class Config(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL") or "sqlite:///" + os.path.join(
        basedir, "prod.db"
    )
    SQLALCHEMY_ECHO = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or ""
    SECRET_KEY = os.getenv("SECRET_KEY") or ""
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT") or ""


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "dev.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL") or "sqlite:///" + os.path.join(
        basedir, "test.db"
    )
    JJWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or ""
    SECRET_KEY = os.getenv("SECRET_KEY") or ""
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT") or ""


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
