import logging
import pytest
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient
from app.utilities.section_enriched import \
    update_section_data_with_enriched_data
from app.tests.data.section_mock_data import section_data, clinical_values, \
    enriched_data
import json

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")


@pytest.mark.parametrize("doc_id, link_level, link_id, user_id, protocol, status_code, comments", [
    ("56f6ba1b-b5b5-40f7-a9bb-0a511fe8657d", '3', "d3795bb7-fe08-11ed-835c-005056ab6469", "Dig2_Batch_Tester",
     "cicl.06ed2096-0749-4ead-a892-9e57ead4fcbc", 200, "doc id and with link id and link_level 3"),
    ("1698be28-1cf3-466e-8f56-5fc920029056", "1", "", "1036048",
     "FEED_TEST4", 404, "doc id changes"),
    ("56f6ba1b-b5b5-40f7-a9bb-0a511fe8657d", "1", "d3795bb7-fe08-11ed-835c-005056ab6469", "Dig2_Batch_Tester",
     "cicl.06ed2096-0749-4ead-a892-9e57ead4fcbc", 200, "doc id and link id present with level 1 all data"),
    ("4c7ea27b-8a6b-4bf0-a8ed-2c1e49bbdc8c", "1", "46bac1b7-9197-11ed-b507-005056ab6469", "Dig2_Batch_Tester",
     "005", 200, "doc id and link id with enriched data")
])
def test_document_object(new_token_on_headers, user_id, protocol, doc_id, status_code, link_level, link_id, comments):
    """
        Tests document Section/Header data for document with doc_id, protocol, user_id, link_level and link_id.
    """
    get_cpt_section_data = client.get("/api/cpt_data/get_section_data/", params={
                                      "aidoc_id": doc_id, "link_level": link_level, "link_id": link_id, "userId": user_id, "protocol": protocol}, headers=new_token_on_headers)
    
    res=json.loads(get_cpt_section_data.text)
    assert get_cpt_section_data.status_code == status_code


# @pytest.mark.parametrize("section_data, enriched_data, result", [
#     (section_data, [], clinical_values),
#     (section_data, enriched_data, clinical_values),
# ])
# def test_section_data_with_enriched_content(section_data, enriched_data, result):
#     response = update_section_data_with_enriched_data(section_data, enriched_data)
#     if enriched_data:
#         assert response[0].get('clinical_terms') == clinical_values
#     else:
#         assert response[0].get('clinical_terms') is None
