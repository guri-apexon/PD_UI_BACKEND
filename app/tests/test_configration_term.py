import logging
import pytest
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")


@pytest.mark.parametrize("doc_id, link_level, link_id, user_id, protocol,config_variables,section_text ,status_code, comments", [
    ("5c784c05-fbd3-4786-b0e4-3afa0d1c61ac", "1", "", "1034911",
     "SSRUT_GEN_001","","", 200, "doc id and without link id"),
    ("1698be28-1cf3-466e-8f56-5fc920029056", "1", "", "1036048",
     "FEED_TEST4","","", 200, "doc id changes"),
    ("21552918-f506-43d8-8879-4fe532631ba7", "", "8f8e70a7-cb76-4257-b595-80a2564a8aa2", "Dig2_Batch_Tester",
     "BI.Obesity.91af1307-5fc5-40cd-9671-b82771a42b2f","","", 200, "doc id and link id present"),
    ("00d9456f-b5d3-4045-b76f-3bdecbe99775","","","1150903","005",
     "clinical_terms,time_points,preferred_terms,redaction_attributes,references,properties","",200,"all configration variables"),
    ("00d9456f-b5d3-4045-b76f-3bdecbe99775","","","1150903","005",
     "clinical_terms,time_points,preferred_terms,redaction_attributes,references,properties","Protocol H9X-MC-GBGJ (a)",200,"all configration variables with section text"),
    ("00d9456f-b5d3-4045-b76f-3bdecbe99775","","","1150903","005",
     "clinical_terms,time_points,preferred_terms,redaction_attributes,references,properties","",200,"all configration variables with link id")
])
def test_configration_variables(new_token_on_headers, user_id, protocol, doc_id, status_code, link_level, link_id, config_variables,section_text ,comments):
    """
        Tests document Section/Header data for document with doc_id, protocol, user_id, link_level and link_id.
    """
    get_config_variables = client.get("/api/cpt_data/get_section_data_configurable_parameter/", params={
                                      "aidoc_id": doc_id, "linklevel": link_level, "linlid": link_id, "userId": user_id, "protocol": protocol, "section_text": section_text, "config_variables": config_variables}, headers=new_token_on_headers)
    assert get_config_variables.status_code == status_code
    