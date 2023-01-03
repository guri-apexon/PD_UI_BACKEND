import logging
import pytest
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")


@pytest.mark.parametrize("doc_id, link_level, toc, status_code, comments", [
    ("5c784c05-fbd3-4786-b0e4-3afa0d1c61ac", "1", "1", 200,
     "doc older than legacy_upload_date for secondary users"),
    ("1698be28-1cf3-466e-8f56-5fc920029057", "1",
     "1", 200, "doc newer than legacy_upload_date"),
    ("1698be28-1cf3-466e-8f56-5fc9200290571", "1",
     "1", 206, "doc newer than legacy_upload_date"),
    ("1698be28-1cf3-466e-8f56-5fc920029057", "1", "2", 206, "doc newer than legacy_upload_date")])
def test_document_header(new_token_on_headers, doc_id, link_level, toc, status_code, comments):
    """
        Tests CPT Sections/Headers  list for a particular document with doc_id, link_level, toc, and comments.
    """
    get_cpt = client.get("/api/cpt_data/", params={
                         "aidoc_id": doc_id, "linklevel": link_level, "toc": toc}, headers=new_token_on_headers)
    assert get_cpt.status_code == status_code
