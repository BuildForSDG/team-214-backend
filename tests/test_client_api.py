import json
import unittest

from sme_financing.main import create_app, db
from sme_financing.main.api_v1 import blueprint as api_v1


class TestClient(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.app.register_blueprint(api_v1)
        self.app.app_context().push()
        db.create_all()
        self.client = self.app.test_client()
        self.baseURL = "http://localhost:5000/api/v1.0/clients/"
        self.headers = {"Content-Type": "application/json"}
        self.payload = json.dumps(
            {
                "lastname": "herve",
                "firstname": "herve",
                "gender": "male",
                "postal_address": "12 po box 78",
                "residential_address": "Accra",
                "telephone": "+233358569587",
                "nationality": "Ghana",
                "education_level": "Masters Degree",
                "position": "CTO",
                "user": {
                    "email": "herve@gmail.com",
                    "username": "herve",
                    "password": "herve",
                    "public_id": "herve",
                },
            }
        )

    def tearDown(self):
        db.drop_all()

    def test_get_list(self):
        res = self.client.get(self.baseURL, headers=self.headers,)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["data"], [])

    def test_create_client(self):
        res = self.client.post(self.baseURL, headers=self.headers, data=self.payload,)
        self.assertEqual(res.status_code, 201)
        self.assertIn("success", str(res.data))
