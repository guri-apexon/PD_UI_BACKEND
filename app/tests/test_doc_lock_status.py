import logging
import pytest
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient
from fastapi import status


client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")


@pytest.mark.parametrize(
    "doc_id, user_id ,status_code",
    [
        ("12b745f9-f1b7-47cd-a165-2a09932e47f1", "u1123897", status.HTTP_200_OK),  #Positive Case
        ("3b44c1d5-f5f7-44ab-901a-3f53c2ba751d", "", status.HTTP_200_OK)  #Negetive Case
    ]
)
def test_create_labdata(doc_id, user_id,status_code, new_token_on_headers):
    get_doc_status = client.get("api/section_lock/document_lock_status", params={
        "doc_id": doc_id,
        "user_id": user_id
        }, headers=new_token_on_headers)
    assert get_doc_status.status_code == status_code
    if get_doc_status.status_code == 200:
        if user_id:
            assert get_doc_status.json()["document_lock_status"] == True
        else:
            assert get_doc_status.json()["document_lock_status"] == False


