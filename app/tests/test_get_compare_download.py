import pytest
from app.api.endpoints import document_compare
from app.db.session import SessionLocal
from fastapi import HTTPException
from app.main import app
from app import config
from fastapi.testclient import TestClient
from fastapi import status

db = SessionLocal()
client = TestClient(app)


@pytest.mark.parametrize("id1, id2, user_id, protocol, status_code",[
    ("e8a66b4f-aa2e-497f-a40e-5d8e0350c0a7", "3b2bf59f-f25b-4308-95eb-2df3ec721d04", "q1036048", "AKB-6548-CI-0014", 200),
    ("e8a66b4f-aa2e-497f-a40e-5d8e0350c0a7", "3b2bf59f-f25b-4308-95eb-2df3ec721d04", "q1021402", "protocol1", 200),
    ("", "3b2bf59f-f25b-4308-95eb-2df3ec721d04", "q1021402", "protocol1", 404),
    ("e8a66b4f-aa2e-497f-a40e-5d8e0350c0a7", "", "q1021402", "protocol1", 404),
    ("e8a66b4f-aa2e-497f-a40e-5d8e0350c0a7", "3b2bf59f-f25b-4308-95eb-2df3ec721d04", "", "protocol1", 404),
    ("e8a66b4f-aa2e-497f-a40e-5d8e0350c0a7", "3b2bf59f-f25b-4308-95eb-2df3ec721d04", "q1021402", "", 404),
    ("e8a66b4f-aa2e-497f-a40e-5d8e0350c0a7", "", "", "", 404),
    ("", "", "", "", 404)
])
def test_get_compare(new_token_on_headers, id1, id2, user_id, protocol, status_code):
    download_response = client.get("/api/document_compare/", params={"id1": id1,  "id2": id2, "user_id": user_id, "protocol_number": protocol}, headers = new_token_on_headers)
    assert download_response.status_code == status_code
    
    if status_code == status.HTTP_200_OK:
        assert download_response.headers['content-length'] != 0
