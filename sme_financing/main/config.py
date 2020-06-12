import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

env_path = os.path.join(basedir, "../../.env")
load_dotenv(dotenv_path=env_path)
print(env_path)


class Config(object):
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_NAME = os.getenv("DB_NAME")


class CloudConfig(Config):
    cloud_sql_connection_name = os.getenv("CLOUD_SQL_CONN_NAME")
    socket = f"unix_socket=/cloudsql/{cloud_sql_connection_name}"
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{Config.DB_USER}:{Config.DB_PASS}@/{Config.DB_NAME}?{socket}"
    )


class ProductionConfig(Config):
    DEBUG = False
    DB_HOST = os.getenv("DB_HOST")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{Config.DB_USER}:{Config.DB_PASS}@{DB_HOST}/{Config.DB_NAME}"
    )
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT") or ""
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or ""
    SECRET_KEY = os.getenv("SECRET_KEY") or ""


class DevelopmentConfig(Config):
    DEBUG = True
    DB_HOST = os.getenv("DB_HOST")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{Config.DB_USER}:{Config.DB_PASS}@{DB_HOST}/{Config.DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "test.db")
    JJWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or ""
    SECRET_KEY = os.getenv("SECRET_KEY") or ""
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT") or ""


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "cloud": CloudConfig,
    "default": DevelopmentConfig,
}
