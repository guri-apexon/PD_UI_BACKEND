import json
import pytest
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient
from fastapi import status
from app.models.pd_nlp_entity_db import NlpEntityDb
from app.crud.pd_nlp_entity_data import nlp_entity_content
from app.models.pd_documenttables_db import DocumenttablesDb

client = TestClient(app)
db = SessionLocal()


def collect_protocol_data():
    enriched_text = 'test_enriched_text'
    rec_id = '2560a040-bc71-11ed-TEST_ID'
    entity_obj = db.query(NlpEntityDb).filter(NlpEntityDb.id == rec_id).first()
    if not entity_obj:
        entity_obj = NlpEntityDb(id=rec_id,
                                 doc_id='4c7ea27b-8a6b-4bf0-a8ed-test',
                                 link_id='46bac1b7-9197-11ed-b507-test',
                                 hierarchy='document',
                                 iqv_standard_term='preferred1',
                                 parent_id='parent_id_test', group_type='',
                                 entity_class='class1', entity_xref='test1',
                                 ontology='MEDra',
                                 standard_entity_name=enriched_text,
                                 confidence=100, start=0, text_len=18)

        try:
            db.add(entity_obj)
            db.commit()
            db.refresh(entity_obj)
        except Exception as ex:
            db.rollback()

    doc_id = entity_obj.doc_id
    link_id = entity_obj.link_id
    enriched_text = entity_obj.standard_entity_name
    return [(doc_id, link_id, enriched_text, '', status.HTTP_200_OK),
            (doc_id, link_id, enriched_text, "0a55c529-fee8-11ed-a5c3-005056ab6469", status.HTTP_200_OK),
            (doc_id, link_id, enriched_text, link_id, status.HTTP_401_UNAUTHORIZED)]


@pytest.mark.parametrize("doc_id, link_id, enriched_text, header_link_id, status_code",
                         collect_protocol_data())
def test_create_new_entity(doc_id, link_id, enriched_text,
                           status_code, header_link_id,new_token_on_headers):
    """ To verify newly created entity with updated clinical terms """
    create_entity = client.post("/api/cpt_data/update_enriched_data",
                                params={"doc_id": doc_id, "link_id": link_id, "header_link_id": header_link_id},
                                json={
                                    "data" : {
                                        "standard_entity_name": "emicizumab",
                                        "iqv_standard_term": "emicizumab_Prefer",
                                        "clinical_terms": "emicizumab_clci_n    ew_last",
                                        "ontology": "emicizumab_ont",
                                        "confidence": "100",
                                        "start": "0",
                                        "text_len": "10",
                                        "parent_id": "1ae04d41-3c52-4e56-8ada-2006c2290c50",
                                        "doc_id": "5a5db927-74b3-4b5a-8d2b-ad022d01c967",
                                        "link_id": "5d5e6dd2-7b35-4c1d-b3d8-98b0bc914f5a",
                                        "synonyms": "",
                                        "classification": "",
                                        "preferred_term": "test_new_1",
                                        "entity_class": "",
                                        "entity_xref": "",
                                        "user_id": "1156301",
                                        "hierarchy": "paragraph"
                                    }
                                },
                                headers=new_token_on_headers)
    if create_entity.status_code == status.HTTP_200_OK:
        response = json.loads(create_entity.text)
        ids = response.get('id')
        _ = db.query(NlpEntityDb).filter(NlpEntityDb.id.in_(ids)).delete()
        db.commit()

    assert create_entity.status_code == status_code


@pytest.mark.parametrize("doc_id, link_id, comments",
                         [
                             ("5a5db927-74b3-4b5a-8d2b-ad022d01c967", "5d5e6dd2-7b35-4c1d-b3d8-98b0bc914f5a", "count nlp entites with nlp get function")
                         ])
def test_get_nlp_record(doc_id, link_id, comments):
    get_records_count = len(nlp_entity_content.get(db, doc_id, link_id))
    assert get_records_count <= db.query(NlpEntityDb).filter(
            NlpEntityDb.doc_id == doc_id).filter(
            NlpEntityDb.link_id == link_id).distinct(NlpEntityDb.parent_id).count()