import json

from .base_test import BaseTest


class TestFundingDetailAPI(BaseTest):

    BASE_URL = "http://localhost:5000/api/v1.0/clients/"
    payload = json.dumps({})

    def test_get(self):
        pass

    def test_get_list(self):
        res = self.client.get(self.baseURL, headers=self.headers,)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.data)["data"], [])

    def test_create_funding_detail(self):
        pass

    def test_delete(self):
        pass

    def test_patch(self):
        pass
