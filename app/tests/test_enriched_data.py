import pytest
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
db = SessionLocal()


@pytest.mark.parametrize("doc_id, link_id, status_code, comments",
                         [("5c784c05-fbd3-4786-b0e4-3afa0d1c61ac", "", 200,
                           "doc id and without link id"), (
                          "1698be28-1cf3-466e-8f56-5fc920029056", "", 200,
                          "doc id changes"), (
                          "21552918-f506-43d8-8879-4fe532631ba7",
                          "8f8e70a7-cb76-4257-b595-80a2564a8aa2", 200,
                          "doc id and link id present")])
def test_document_data(new_token_on_headers, doc_id, status_code, link_id,
                       comments):
    """
    Tests document enriched data for document with doc_id, link_id.
    """
    get_enriched_data = client.get("/api/cpt_data/get_enriched_terms",
                                   params={"aidoc_id": doc_id,
                                           "linkid": link_id},
                                   headers=new_token_on_headers)

    assert get_enriched_data.status_code == status_code
