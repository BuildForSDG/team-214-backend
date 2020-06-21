import io
import json

baseURL = "/api/v1.0/documents/"
headers = {"Content-Type": "multipart/form-data"}


def test_success_get_empty_list_documents(test_client, init_db):
    res = test_client.get(baseURL)
    assert res.status_code == 200
    assert json.loads(res.data)["data"] == []


def test_success_save_document(test_client, init_db, tmp_path):
    payload = {"document_name": "Balance Sheet 2020"}
    payload["file"] = (io.BytesIO(b"balancesheet"), f"{tmp_path}/sub/balancesheet.txt")
    res = test_client.post(baseURL, headers=headers, data=payload)
    assert res.status_code == 201
    assert "success" in str(res.data)


def test_404_save_document(test_client, init_db):
    payload = {"document_name": "Balance Sheet 2020"}
    res = test_client.post(baseURL, headers=headers, data=payload)
    assert res.status_code == 404
    assert "not found" in str(res.data)
