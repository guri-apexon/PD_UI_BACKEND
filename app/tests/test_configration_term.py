import logging
import pytest
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient
from app.tests.data.section_mock_data import configuration_api_data
from fastapi import status

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")


@pytest.mark.parametrize("doc_id, link_level, link_id, user_id, protocol,config_variables,section_text ,status_code, comments", configuration_api_data)
def test_configration_variables(new_token_on_headers, user_id, protocol, doc_id, status_code, link_level, link_id, config_variables,section_text ,comments):
    """
        Tests document Section/Header data for document with doc_id, protocol, user_id, link_level and link_id.
    """
    get_config_variables = client.get("/api/cpt_data/get_section_data_configurable_parameter/", params={
                                      "aidoc_id": doc_id, "linklevel": link_level, "link_id": link_id, "userId": user_id, "protocol": protocol, "section_text": section_text, "config_variables": config_variables}, headers=new_token_on_headers)
    
    
    if status_code == status.HTTP_404_NOT_FOUND:
        assert get_config_variables.json()[0]['status_code'] == status_code
        
    elif comments == "NO_TIME_POINT_DATA":
        assert 'time_points' not in get_config_variables.json()[1][0].keys()
    
    elif comments == "NO_REFERENCE_DATA":
        assert 'references' not in get_config_variables.json()[1][0].keys()

    else:
        assert get_config_variables.status_code == status_code

