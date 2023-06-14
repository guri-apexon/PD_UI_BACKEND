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

@pytest.mark.parametrize("section_lock_test_data", [(r"./app/tests/data/section_lock_false_put.json"), (r"./app/tests/data/section_lock_true_put.json")])
def test_section_lock_put_curd_fail(new_token_on_headers, section_lock_test_data):
    """
        update section lock
    """
    with open(section_lock_test_data, 'r') as f:
        data = f.read()
        test_payload_dict = json.loads(data)
    test_payload_dict['link_id'] = None
    test_payload_dict['doc_id'] = None
    put_section_lock = client.put(
        TEST_END_POINT_PUT, json=test_payload_dict, headers=new_token_on_headers)
    assert put_section_lock.status_code == 500


TEST_END_POINT_GET = "/api/section_lock/get_section_lock"


@pytest.mark.parametrize("section_lock_test_data", [(r"./app/tests/data/section_lock_get.json")])
def test_section_lock_get_curd_fail(new_token_on_headers, section_lock_test_data):
    """
        get section lock info
    """
    with open(section_lock_test_data, 'r') as f:
        data = f.read()
        test_payload_dict = json.loads(data)
    test_payload_dict['link_id'] = ''
    test_payload_dict['doc_id'] = ''
    get_section_lock = client.get(
        TEST_END_POINT_GET, params=test_payload_dict, headers=new_token_on_headers)
    assert get_section_lock.status_code == 500


@pytest.mark.parametrize("submit_protocol_workflow_data", [(r"./app/tests/data/submit_protocol_workflow_data.json")])
def test_submit_protocol_workflow(new_token_on_headers, submit_protocol_workflow_data, mocker):
    """
    Test SubmitProtocolWorkflow endpoint
    """
    # Load test data from JSON file
    with open(submit_protocol_workflow_data, 'r') as f:
        data = f.read()
        test_payload_dict = json.loads(data)

    # Mock the section_lock_service.remove function
    mocked_remove = mocker.patch('app.routers.section_lock.section_lock_service.remove')
    mocked_remove.return_value = {"message": "Lock removed successfully."}, True

    # Send a request to the SubmitProtocolWorkflow endpoint
    response = client.post(
        "/api/section_lock/submit_protocol_workflow",
        json=test_payload_dict,
        headers=new_token_on_headers
    )

    # Assert the response status code is 200
    assert response.status_code == 200

    # Assert the response body
    response_data = response.json()
    assert response_data == {"success": True, "info": "Lock removed successfully."}

    # Assert that the section_lock_service.remove function was called with the correct payload
    mocked_remove.assert_called_once_with(test_payload_dict)
