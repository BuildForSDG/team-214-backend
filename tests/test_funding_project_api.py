import json
import unittest

from sme_financing.main import create_app, db
from sme_financing.main.api_v1 import blueprint as api_v1

BASE_URL = "http://127.0.0.1:5000/api/v1.0/"


class TestFundingProject(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.app.register_blueprint(api_v1)
        self.app.app_context().push()
        db.create_all()
        self.client = self.app.test_client()
        self.baseURL = "http://localhost:5000/api/v1.0/funding_projects/"
        self.headers = {"Content-Type": "application/json"}
        self.funding_project = json.dumps(
            {
                "number": "FP12 2020",
                "title": "Funding Project kick ass",
                "description": "Yeah the desc is dope",
                "relevance": "Yeah it's relevance",
                "objectives": "Yeah the objectives are dope",
                "justification": "Yeah the justification is dope",
                "work_plan": "Yeah the work_plan is dope",
                "status": "In Progress",
                "fund_amount": 125800,
                "start_date": "2020-06-04",
                "end_date": "2020-12-04",
                "investor_email": "boa@gmail.com",
                "funding_application_number": "FA 1A 2020",
            }
        )

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_list(self):
        res = self.client.get(self.baseURL, headers=self.headers,)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["data"], [])

    def test_create_funding_project(self):
        res = self.client.post(
            self.baseURL, headers=self.headers, data=self.funding_project,
        )
        self.assertNotEqual(res.status_code, 201)
        self.assertIn("error", json.loads(res.data)["status"])
