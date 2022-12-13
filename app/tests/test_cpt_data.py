import logging

import pytest
from app.db.session import SessionLocal
from app.main import app

from fastapi.testclient import TestClient

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")


@pytest.mark.parametrize("doc_id, link_level, status_code, comments", [
    ("5c784c05-fbd3-4786-b0e4-3afa0d1c61ac", "1",  401, "doc older than legacy_upload_date for secondary users"),
    ("1698be28-1cf3-466e-8f56-5fc920029057", "1",  200, "doc newer than legacy_upload_date")
])
def test_old_processed_doc(new_token_on_headers, user_id, protocol, doc_id, user_type, status_code, comments):

    get_cpt = client.get("/api/cpt_data/", params={"aidoc_id": doc_id, "linklevel": link_level, }, headers = new_token_on_headers)
    assert get_cpt.status_code == status_code
