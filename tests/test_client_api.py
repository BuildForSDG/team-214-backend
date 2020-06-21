import json

baseURL = "/api/v1.0/clients/"
headers = {"Content-Type": "application/json"}
payload = {
    "lastname": "Client1_lastname",
    "firstname": "Client1_firstname",
    "gender": "male",
    "postal_address": "12 PO BOX 78",
    "residential_address": "Accra",
    "telephone": "+233358569587",
    "nationality": "Ghana",
    "education_level": "Masters Degree",
    "position": "CTO",
    "user": {
        "email": "client_user1@email.com",
        "username": "user1",
        "password": "user1",
        "public_id": "user1",
    },
}


def test_success_get_empty_list_clients(test_client, init_db):
    assert test_client is not None
    res = test_client.get(baseURL)
    assert res.status_code == 200
    assert json.loads(res.data)["data"] == []


def test_success_create_client(test_client, init_db):
    res = test_client.post(baseURL, headers=headers, data=json.dumps(payload))
    assert res.status_code == 201
    assert "success" in str(res.data)


def test_conflict_create_existing_client(test_client, init_db):
    res = test_client.post(baseURL, headers=headers, data=json.dumps(payload))
    assert res.status_code == 409
    assert "error" in str(res.data)


def test_success_create_client2(test_client, init_db):
    payload["lastname"] = "Client1_lastname"
    payload["firstname"] = "Client1_firstname"
    payload["user"]["email"] = "client_user2@email.com"
    payload["user"]["username"] = "user2"
    payload["user"]["password"] = "user2"
    payload["user"]["public_id"] = "user2"

    res = test_client.post(baseURL, headers=headers, data=json.dumps(payload))
    assert res.status_code == 201
    assert "success" in str(res.data)


def test_success_get_list_client(test_client, init_db):
    res = test_client.get(baseURL, headers=headers,)
    assert res.status_code == 200
    data = json.loads(res.data)["data"]
    assert len(data) == 2
    assert data[0]["firstname"] == "Client1_firstname"
    assert data[1]["user"]["email"] == "client_user2@email.com"


def test_get_client_by_email(test_client, init_db):
    res = test_client.get(baseURL + "email/client_user1@email.com", headers=headers,)
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["firstname"] == "Client1_firstname"
    assert data["user"]["email"] == "client_user1@email.com"
