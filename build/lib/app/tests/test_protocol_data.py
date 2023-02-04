import logging

import pytest
from app.db.session import SessionLocal
from app.main import app

from fastapi.testclient import TestClient

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")


@pytest.mark.parametrize("doc_id, user_id, protocol, user_type, status_code, comments", [
    ("5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "1034911", "SSRUT_GEN_001", "normal", 401, "doc older than legacy_upload_date for secondary users"),
    ("c6f3ed89-b77b-49d0-b72b-6d901a727a43", "1036048", "FEED_TEST4", "normal", 200, "doc newer than legacy_upload_date")
])
def test_old_processed_doc(new_token_on_headers, user_id, protocol, doc_id, user_type, status_code, comments):

    get_protocols = client.get("/api/protocol_data/", params={"aidoc_id": doc_id, "userId": user_id, "protocol": protocol, "user": user_type}, headers = new_token_on_headers)
    assert get_protocols.status_code == status_code
