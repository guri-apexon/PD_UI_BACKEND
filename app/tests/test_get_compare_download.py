import pytest
from app.api.endpoints import document_compare
from app.db.session import SessionLocal
from fastapi import HTTPException
from app.main import app
from fastapi.testclient import TestClient
from fastapi import status

db = SessionLocal()
client = TestClient(app)


@pytest.mark.parametrize("id1, id2, status_code, content_length",[
    ("0197a592-cc88-40cd-aabd-b202e17760d6", "f5798903-7034-4975-a97d-7cb8e8fb8aa2", 200, '463479'),
    ("1", "2", 404, ''),
    ("", "", 404, '')
])
def test_get_compare(new_token_on_headers, id1, id2, status_code, content_length):
    download_response = client.get("/api/document_compare/", params={"id1": id1,  "id2": id2}, headers = new_token_on_headers)
    assert download_response.status_code == status_code
    
    if status_code == status.HTTP_200_OK:
        assert download_response.headers['content-length'] == content_length
