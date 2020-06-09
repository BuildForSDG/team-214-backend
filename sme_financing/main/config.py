import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

env_path = os.path.join(basedir, "../../.env")
load_dotenv(dotenv_path=env_path)
print(env_path)


class Config(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class CloudConfig(Config):
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_name = os.environ.get("DB_NAME")
    cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONN_NAME")
    socket = f"unix_socket=/cloudsql/{cloud_sql_connection_name}"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_pass}@/{db_name}?{socket}"


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
