import unittest

from sme_financing.main import create_app, db


class BaseTest(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.app.app_context().push()
        db.create_all()
        self.client = self.app.test_client()
        self.headers = {"Content-Type": "application/json"}

    def tearDown(self):
        db.session.remove()
        db.drop_all()
