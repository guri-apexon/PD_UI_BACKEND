from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_ldap_user_details(new_token_on_headers):
    input_json = {
        "userId": "ypd"
    }

    response = client.post("/api/ldap_user_details/", params=input_json, headers=new_token_on_headers)
    assert response.status_code == 200


def test_get_ldap_invalid_user_details(new_token_on_headers):
    input_json = {
        "userId": "XXX"
    }

    expected_json = {
        'detail': 'No record found for userId: XXX'
    }

    response = client.post("/api/ldap_user_details/", params=input_json, headers=new_token_on_headers)
    assert response.status_code == 403
    assert response.json() == expected_json

