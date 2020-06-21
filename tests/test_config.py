from sme_financing.main import create_app


def test_app_is_development():
    app = create_app(config_name="development")
    assert app is not None
    assert app.config["DEBUG"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] is not None


def test_app_is_testing():
    app = create_app(config_name="testing")
    assert app is not None
    assert app.config["TESTING"] is True


def test_app_is_production():
    app = create_app(config_name="production")
    assert app is not None
    assert app.config["DEBUG"] is False
    assert app.config["SQLALCHEMY_DATABASE_URI"] is not None
