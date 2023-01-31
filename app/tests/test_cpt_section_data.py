import logging
import pytest
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient
from app.utilities.section_enriched import \
    update_section_data_with_enriched_data
from app.tests.data.section_mock_data import section_data, clinical_values, \
    enriched_data

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")


@pytest.mark.parametrize("doc_id, link_level, link_id, user_id, protocol, status_code, comments", [
    ("5c784c05-fbd3-4786-b0e4-3afa0d1c61ac", "1", "", "1034911",
     "SSRUT_GEN_001", 200, "doc id and without link id"),
    ("1698be28-1cf3-466e-8f56-5fc920029056", "1", "", "1036048",
     "FEED_TEST4", 404, "doc id changes"),
    ("21552918-f506-43d8-8879-4fe532631ba7", "", "8f8e70a7-cb76-4257-b595-80a2564a8aa2", "Dig2_Batch_Tester",
     "BI.Obesity.91af1307-5fc5-40cd-9671-b82771a42b2f", 200, "doc id and link id present"),
    ("4c7ea27b-8a6b-4bf0-a8ed-2c1e49bbdc8c", "1", "46bac1b7-9197-11ed-b507-005056ab6469", "Dig2_Batch_Tester",
     "005", 200, "doc id and link id with enriched data")
])
def test_document_object(new_token_on_headers, user_id, protocol, doc_id, status_code, link_level, link_id, comments):
    """
        Tests document Section/Header data for document with doc_id, protocol, user_id, link_level and link_id.
    """
    get_cpt_section_data = client.get("/api/cpt_data/get_section_data/", params={
                                      "aidoc_id": doc_id, "linklevel": link_level, "linlid": link_id, "userId": user_id, "protocol": protocol}, headers=new_token_on_headers)
    assert get_cpt_section_data.status_code == status_code


@pytest.mark.parametrize("section_data, enriched_data, result", [
    (section_data, [], clinical_values),
    (section_data, enriched_data, clinical_values),
])
def test_section_data_with_enriched_content(section_data, enriched_data, result):
    response = update_section_data_with_enriched_data(section_data, enriched_data)
    if enriched_data:
        assert response[0].get('clinical_terms') == clinical_values
    else:
        assert response[0].get('clinical_terms') is None
