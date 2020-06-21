import pytest

from sme_financing.main import create_app, db


@pytest.fixture(scope="session")
def app():
    flask_app = create_app(config_name="testing")

    ctx = flask_app.app_context()
    ctx.push()

    yield flask_app

    ctx.pop()


@pytest.fixture(scope="session")
def test_client(app):
    flask_app = create_app(config_name="testing")
    test_client = flask_app.test_client()

    with app.test_client() as test_client:
        yield test_client


@pytest.fixture(scope="session")
def init_db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="class")
def app_testing(request):
    app = create_app(config_name="testing")
    request.cls.app = app
