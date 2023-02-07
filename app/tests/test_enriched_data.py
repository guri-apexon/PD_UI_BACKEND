import json
import pytest
from app.db.session import SessionPSQL
from app.main import app
from fastapi.testclient import TestClient
from fastapi import status
from app.models.pd_nlp_entity_db import NlpEntityDb

client = TestClient(app)
db = SessionPSQL()


@pytest.mark.parametrize("doc_id, link_id, status_code, comments",
                         [("5c784c05-fbd3-4786-b0e4-3afa0d1c61ac", "", 200,
                           "doc id and without link id"), (
                          "1698be28-1cf3-466e-8f56-5fc920029056", "", 200,
                          "doc id changes"), (
                          "21552918-f506-43d8-8879-4fe532631ba7",
                          "8f8e70a7-cb76-4257-b595-80a2564a8aa2", 200,
                          "doc id and link id present"),
                          ("4c7ea27b-8a6b-4bf0-a8ed-2c1e49bbdc8c",
                           "46bac1b7-9197-11ed-b507-005056ab6469", 200,
                           "doc id and link id with enriched data")
                          ])
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


def collect_protocol_data():
    entity_obj = db.query(NlpEntityDb).first()
    doc_id = entity_obj.doc_id
    link_id = entity_obj.link_id
    enriched_text = entity_obj.standard_entity_name
    return doc_id, link_id, enriched_text, status.HTTP_200_OK


@pytest.mark.parametrize("doc_id, link_id, enriched_text, status_code",
                         [collect_protocol_data()])
def test_create_new_entity(doc_id, link_id, enriched_text,
                           status_code, new_token_on_headers):
    """ To verify newly created entity with updated clinical terms """
    create_entity = client.post("/api/cpt_data/update_enriched_data",
                                params={"doc_id": doc_id, "link_id": link_id},
                                json={"data": {
                                    "standard_entity_name": enriched_text,
                                    "iqv_standard_term": "", "entity_class": "",
                                    "entity_xref": "test1, test2",
                                    "ontology": ""}},
                                headers=new_token_on_headers)
    if create_entity.status_code == status.HTTP_200_OK:
        response = json.loads(create_entity.text)
        ids = response.get('id')
        _ = db.query(NlpEntityDb).filter(NlpEntityDb.id.in_(ids)).delete()
        db.commit()
    assert create_entity.status_code == status.HTTP_200_OK
