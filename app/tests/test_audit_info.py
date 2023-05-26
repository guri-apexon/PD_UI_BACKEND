import logging
import pytest
import json
import uuid 
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
logger = logging.getLogger("unit-test")

TEST_END_POINT_AUDIT_INFO = "/api/audit_info/get_audit_info"

TEST_END_POINT_QC_INGEST = "/api/qc_ingest/"

def get_qc_ingest_api_response(payload, new_token_on_headers):
    qc_ingest = client.post(
        TEST_END_POINT_QC_INGEST, json=[payload], headers=new_token_on_headers)
    return qc_ingest
    

def get_audit_info_api_response(payload, new_token_on_headers):
    put_audit_info = client.get(
            TEST_END_POINT_AUDIT_INFO, params=payload, headers=new_token_on_headers)
    return put_audit_info


@pytest.mark.parametrize("qc_ingest_test_data, audit_info_test_data", [(r"./app/tests/data/qc_ingest_text_curd_data.json",r"./app/tests/data/audit_info_curd_data.json")])
def test_verify_audit_log_curd(new_token_on_headers, qc_ingest_test_data, audit_info_test_data):
    """
        verify audit info
    """
    curr_uid = str(uuid.uuid4())
    logger.info(f'current uid is {curr_uid}')
    with open(audit_info_test_data, 'r') as f:
        data_audit = f.read()
        test_payload_dict_audit = json.loads(data_audit)
    audit_payload = test_payload_dict_audit[0]
    audit_payload['line_id'] = curr_uid

    with open(qc_ingest_test_data, 'r') as f:
        data = f.read()
        test_payload_list = json.loads(data)
    for i in range(len(test_payload_list)):
        payload = test_payload_list[i]
        if payload.get('line_id', None):
            payload['line_id'] = curr_uid
        else:
            payload['uuid'] = curr_uid
        add_qc_ingest = get_qc_ingest_api_response(payload, new_token_on_headers)
        assert add_qc_ingest.status_code == 200
        if i == 2:
            break
        put_audit_info = get_audit_info_api_response(audit_payload, new_token_on_headers)
        assert put_audit_info.status_code == 200
        audit_info = json.loads(put_audit_info.text)
        assert audit_info['info']['audit_info']['last_reviewed_by'] == payload['audit']['last_updated_user']
        assert audit_info['info']['audit_info']['total_no_review'] == i

@pytest.mark.parametrize("audit_info_test_data", [(r"./app/tests/data/audit_info_curd_data.json")])
def test_audit_info_get_curd(new_token_on_headers, audit_info_test_data):
    """
        get audit info
    """
    with open(audit_info_test_data, 'r') as f:
        data = f.read()
        test_payload_dict = json.loads(data)
    for data in test_payload_dict:
        put_audit_info = get_audit_info_api_response(data, new_token_on_headers)
        assert put_audit_info.status_code == 200
