import json

baseURL = "/api/v1.0/smes/"
headers = {"Content-Type": "application/json"}
payload = {
    "name": "Short stay Accra",
    "postal_address": "12 po box 78",
    "location": "Accra",
    "telephone": "+23369584587",
    "email": "stay@gmail.com",
    "description": "Yeah it's a hotel",
    "sector": "Hotel Business",
    "principal_product_service": "Hotel",
    "other_product_service": "Restaurant",
    "age": "More than 24 months",
    "establishment_date": "2019-07-11",
    "ownership_type": "LLC",
    "bank_account_details": "789568521524",
    "employees_number": 24,
    "client_email": "client_user1@email.com",
    "client_id": 1,
}


def test_success_get_empty_list_smes(test_client, init_db):
    assert test_client is not None
    res = test_client.get(baseURL)
    assert res.status_code == 200
    assert json.loads(res.data)["data"] == []


def test_success_create_sme(test_client, init_db):
    res = test_client.post(baseURL, headers=headers, data=json.dumps(payload))
    assert res.status_code == 201
    assert "success" in res.get_data(as_text=True)

    payload["email"] = "sme_email@email.com"
    res = test_client.post(baseURL, headers=headers, data=json.dumps(payload))
    assert res.status_code == 201
    assert "success" in res.get_data(as_text=True)


def test_success_delete_sme(test_client, init_db):
    res = test_client.delete(baseURL + "2")
    assert res.status_code == 200
    assert "success" in res.get_data(as_text=True)


def test_success_patch_sme(test_client, init_db):
    payload["email"] = "newsme@email.com"
    payload["establishment_date"] = "2020-01-11"
    res = test_client.patch(baseURL+ "1", headers=headers, data=json.dumps(payload))
    assert res.status_code == 201
    assert "success" in res.get_data(as_text=True)


def test_success_get_sme_by_id(test_client, init_db):
    res = test_client.get(baseURL + "1", headers=headers,)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["email"] == "newsme@email.com"
    assert data["establishment_date"] == "2020-01-11"


def test_success_get_list_sme(test_client, init_db):
    res = test_client.get(baseURL, headers=headers,)
    assert res.status_code == 200
    data = json.loads(res.data)["data"]
    assert len(data) >= 1


def test_404_get_sme_by_id(test_client, init_db):
    res = test_client.get(baseURL + "100", headers=headers,)
    assert res.status_code == 404
