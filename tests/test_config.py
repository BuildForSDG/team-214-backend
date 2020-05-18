import os
import unittest

from flask import current_app
from flask_testing import TestCase

from manage import app
from sme_financing.main.config import basedir


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object("sme_financing.main.config.DevelopmentConfig")
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config["SECRET_KEY"] == "whatisthat")
        self.assertTrue(app.config["DEBUG"] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config["SQLALCHEMY_DATABASE_URI"]
            == "sqlite:///" + os.path.join(basedir, "dev.db")
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object("sme_financing.main.config.TestingConfig")
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config["SECRET_KEY"] == "my_precious")
        self.assertTrue(app.config["DEBUG"])
        self.assertTrue(
            app.config["SQLALCHEMY_DATABASE_URI"]
            == "sqlite:///" + os.path.join(basedir, "test.db")
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object("sme_financing.main.config.ProductionConfig")
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config["DEBUG"] is False)


if __name__ == "__main__":
    unittest.main()
