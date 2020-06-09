import unittest

from sme_financing.main import create_app, db
from sme_financing.main.api_v1 import blueprint as api_v1


class BaseTest(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.app.register_blueprint(api_v1)
        self.app.app_context().push()
        db.create_all()
        self.client = self.app.test_client()
        self.headers = {"Content-Type": "application/json"}

    def tearDown(self):
        db.session.remove()
        db.drop_all()
