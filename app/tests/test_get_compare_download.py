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


@pytest.mark.parametrize("id1, id2, user_id, protocol, file_type, status_code",[
    ("2e4ea1e9-023e-4d0c-b201-26bd55b1676b", "216d2604-9040-4159-a2c8-8b0993e0b93e", "q1036048", "AKB-6548-CI-0014", ".csv", 200),
    ("2e4ea1e9-023e-4d0c-b201-26bd55b1676b", "216d2604-9040-4159-a2c8-8b0993e0b93e", "q1036048", "AKB-6548-CI-0014", ".xlsx", 200),
    ("2e4ea1e9-023e-4d0c-b201-26bd55b1676b", "216d2604-9040-4159-a2c8-8b0993e0b93e", "q1036048", "AKB-6548-CI-0014", ".tiff", 404),
    ("2e4ea1e9-023e-4d0c-b201-26bd55b1676b", "216d2604-9040-4159-a2c8-8b0993e0b93e", "q1021402", "protocol1", ".csv", 200),
    ("2e4ea1e9-023e-4d0c-b201-26bd55b1676b", "216d2604-9040-4159-a2c8-8b0993e0b93e", "q1021402", "protocol1", ".xlsx", 200),
    ("2e4ea1e9-023e-4d0c-b201-26bd55b1676b", "216d2604-9040-4159-a2c8-8b0993e0b93e", "q1021402", "protocol1", ".tiff", 404),
    ("", "216d2604-9040-4159-a2c8-8b0993e0b93e", "q1021402", "protocol1", ".csv", 404),
    ("2e4ea1e9-023e-4d0c-b201-26bd55b1676b", "", "q1021402", "protocol1", ".csv", 404),
    ("2e4ea1e9-023e-4d0c-b201-26bd55b1676b", "216d2604-9040-4159-a2c8-8b0993e0b93e", "", "protocol1", ".csv", 200),
    ("2e4ea1e9-023e-4d0c-b201-26bd55b1676b", "216d2604-9040-4159-a2c8-8b0993e0b93e", "q1021402", "", ".csv", 200),
    ("2e4ea1e9-023e-4d0c-b201-26bd55b1676b", "", "", "", "", 404),
    ("", "", "", "", "", 404)
])
def test_get_compare(new_token_on_headers, id1, id2, user_id, protocol, file_type, status_code):
    download_response = client.get("/api/document_compare/", params={"id1": id1,  "id2": id2, "userId": user_id, "protocol": protocol, "file_type": file_type}, headers = new_token_on_headers)
    assert download_response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        assert download_response.headers['content-length'] != 0
