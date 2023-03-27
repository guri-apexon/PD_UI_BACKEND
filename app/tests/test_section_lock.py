import logging
import pytest
import json
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
logger = logging.getLogger("unit-test")

TEST_END_POINT_PUT = "/api/section_lock/put_section_lock"


@pytest.mark.parametrize("section_lock_test_data", [(r"./app/tests/data/section_lock_false_put.json"), (r"./app/tests/data/section_lock_true_put.json")])
def test_section_lock_put_curd(new_token_on_headers, section_lock_test_data):
    """
        update section lock
    """
    with open(section_lock_test_data, 'r') as f:
        data = f.read()
        test_payload_dict = json.loads(data)
    put_section_lock = client.put(
        TEST_END_POINT_PUT, json=test_payload_dict, headers=new_token_on_headers)
    assert put_section_lock.status_code == 200


TEST_END_POINT_GET = "/api/section_lock/get_section_lock"


@pytest.mark.parametrize("section_lock_test_data", [(r"./app/tests/data/section_lock_get.json")])
def test_section_lock_get_curd(new_token_on_headers, section_lock_test_data):
    """
        get section lock info
    """
    with open(section_lock_test_data, 'r') as f:
        data = f.read()
        test_payload_dict = json.loads(data)
    get_section_lock = client.get(
        TEST_END_POINT_GET, params=test_payload_dict, headers=new_token_on_headers)
    assert get_section_lock.status_code == 200
