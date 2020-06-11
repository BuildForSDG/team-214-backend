import unittest

from flask import current_app
from flask_testing import TestCase

from manage import app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object("sme_financing.main.config.DevelopmentConfig")
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config["DEBUG"] is True)
        self.assertFalse(current_app is None)
        self.assertIsNotNone(app.config["SQLALCHEMY_DATABASE_URI"])


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object("sme_financing.main.config.TestingConfig")
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config["DEBUG"])


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object("sme_financing.main.config.ProductionConfig")
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config["DEBUG"] is False)
        self.assertIsNotNone(app.config["SQLALCHEMY_DATABASE_URI"])


if __name__ == "__main__":
    unittest.main()
