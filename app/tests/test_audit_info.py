import logging
import pytest
import json
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
logger = logging.getLogger("unit-test")

TEST_END_POINT = "/api/audit_info/get_audit_info"


@pytest.mark.parametrize("audit_info_test_data", [(r"./app/tests/data/audit_info_curd_data.json")])
def test_audit_info_get_curd(new_token_on_headers, audit_info_test_data):
    """
        get audit info
    """
    with open(audit_info_test_data, 'r') as f:
        data = f.read()
        test_payload_dict = json.loads(data)
    for data in test_payload_dict:
        put_section_lock = client.get(
            TEST_END_POINT, json=data, headers=new_token_on_headers)
        assert put_section_lock.status_code == 200
