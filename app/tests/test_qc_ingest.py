import logging
import pytest
import json
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient
from app.qc_ingest.model.documenttables_db import DocTableHelper
from copy import deepcopy
import uuid

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")

TEST_END_POINT = "/api/qc_ingest/"

uid = str(uuid.uuid4())
logging.info(f"uuid is {uid}")


@pytest.mark.parametrize("qc_ingest_test_data", [(r"./app/tests/data/qc_ingest_text_curd_data.json")])
def test_document_line_curd(new_token_on_headers, qc_ingest_test_data):
    """
        create,update,delete line
    """
    curr_uid = str(uuid.uuid4())
    logger.info(f'current uid is {curr_uid}')
    with open(qc_ingest_test_data, 'r') as f:
        data = f.read()
        test_payload_list = json.loads(data)
    for payload in test_payload_list:
        if payload.get('line_id', None):
            payload['line_id'] = curr_uid
        else:
            payload['uuid'] = curr_uid
        get_qc_ingest = client.post(
            TEST_END_POINT, json=[payload], headers=new_token_on_headers)
        assert get_qc_ingest.status_code == 200


@pytest.mark.parametrize("qc_ingest_test_data", [(r"./app/tests/data/qc_ingest_image_curd_data.json")])
def test_document_image_curd(new_token_on_headers, qc_ingest_test_data):
    """

    SELECT * FROM public.iqvdocumentimagebinary_db WHERE "para_id"='mnf5d19t-16f5-4xf2-xe06-35fcc0c0eeux'
    """
    curr_uid = str(uuid.uuid4())
    logger.info(f'current uid is {curr_uid}')
    with open(qc_ingest_test_data, 'r') as f:
        data = f.read()
        test_payload_list = json.loads(data)
    for payload in test_payload_list:
        if payload.get('line_id', None):
            payload['line_id'] = curr_uid
        else:
            payload['uuid'] = curr_uid
        get_qc_ingest = client.post(
            TEST_END_POINT, json=[payload], headers=new_token_on_headers)
        assert get_qc_ingest.status_code == 200


@pytest.mark.parametrize("qc_ingest_test_data", [(r"./app/tests/data/qc_ingest_section_curd_data.json")])
def test_document_section_curd(new_token_on_headers, qc_ingest_test_data):
    """
    Operations read data and does clean up
    For Verification :
    SELECT * FROM public.iqvdocumentlink_db WHERE "id"='34000496-bx4r-1pef-8aab-10505xab64ft'
    SELECT "Value" FROM public.documentparagraphs_db WHERE "id"='34000496-bx4r-1pef-8aab-10505xab64ft'
    SELECT * FROM public.documentpartslist_db WHERE "id"='34000496-bx4r-1pef-8aab-10505xab64ft'
    """
    curr_uid = str(uuid.uuid4())
    logger.info(f'current uid is {curr_uid}')
    with open(qc_ingest_test_data, 'r') as f:
        data = f.read()
        test_payload_list = json.loads(data)
    for payload in test_payload_list:
        if payload.get('link_id', None):
            payload['link_id'] = curr_uid
        else:
            payload['uuid'] = curr_uid
        get_qc_ingest = client.post(
            TEST_END_POINT, json=[payload], headers=new_token_on_headers)
        assert get_qc_ingest.status_code == 200


def get_table_data(uuid):
    helper = DocTableHelper()
    with SessionLocal() as session:
        data = helper.get_table(session, uuid)
        return data


def get_payload(file_name):
    with open(file_name, 'r') as f:
        data = f.read()
        payload = json.loads(data)
        return payload


def create_table(qc_ingest_test_data, new_token_on_headers):
    with open(qc_ingest_test_data, 'r') as f:
        data = f.read()
        payload = json.loads(data)
        payload[0]['uuid'] = uid
        response = client.post(
            TEST_END_POINT, json=payload, headers=new_token_on_headers)
        assert response.status_code == 200
        return payload[0]['uuid']


def delete_table(uuid, new_token_on_headers):
    qc_ingest_test_data = r"./app/tests/data/qc_ingest_table_delete.json"
    payload = get_payload(qc_ingest_test_data)
    payload[0]['line_id'] = uuid
    response = client.post(
        TEST_END_POINT, json=payload, headers=new_token_on_headers)
    assert response.status_code == 200


def modify_data_all(uuid, new_token_on_headers):
    qc_ingest_test_data = r"./app/tests/data/qc_ingest_table_data_modify_table.json"
    payload = get_payload(qc_ingest_test_data)
    payload[0]['line_id'] = uuid
    response = client.post(
        TEST_END_POINT, json=payload, headers=new_token_on_headers)
    assert response.status_code == 200

@pytest.mark.parametrize("qc_ingest_test_data", [
    (r"./app/tests/data/qc_ingest_table_data_create.json")
])
def test_document_table_curd_all_modifiction(new_token_on_headers, qc_ingest_test_data):
    """
    Operations read data and does clean up
    For Verification :
    SELECT * FROM public.iqvdocumentlink_db WHERE "id"='34000496-bx4r-1pef-8aab-10505xab64ft'
    SELECT "Value" FROM public.documentparagraphs_db WHERE "id"='34000496-bx4r-1pef-8aab-10505xab64ft'
    SELECT * FROM public.documentpartslist_db WHERE "id"='34000496-bx4r-1pef-8aab-10505xab64ft'
    """

    uuid = create_table(qc_ingest_test_data, new_token_on_headers)
    modify_data_all(uuid, new_token_on_headers)
    data = get_table_data(uuid)

    assert data[0][0]['val'] == "0 new"
    assert data[0][1]['val'] == '1 new'
    assert data[0][2]['val'] == '2 new'
    assert data[0][3]['val'] == '3 new'
    assert data[0][4]['val'] == "4 new"
    assert data[0][5]['val'] == '5 new'
    assert data[1][0]['val'] == "1"
    assert data[1][1]['val'] == '2'
    assert data[1][2]['val'] == '3 mod'
    assert data[1][3]['val'] == '4'
    assert data[1][4]['val'] == "5 mod"
    assert data[1][5]['val'] == '5'
    assert data[2][0]['val'] == "6 mod"
    assert data[2][1]['val'] == '7 mod'
    assert data[2][2]['val'] == '8 new'
    assert data[2][3]['val'] == '9'
    assert data[2][4]['val'] == "10 new"
    assert data[2][5]['val'] == '10'
    assert data[3][0]['val'] == "11 mod"
    assert data[3][1]['val'] == '12 mod'
    assert data[3][2]['val'] == '13 new'
    assert data[3][3]['val'] == '14'
    assert data[3][4]['val'] == "15 new"
    assert data[3][5]['val'] == '15'
    assert data[4][0]['val'] == "16 mod"
    assert data[4][1]['val'] == '17'
    assert data[4][2]['val'] == '18 new'
    assert data[4][3]['val'] == '19'
    assert data[4][4]['val'] == "20 new"
    assert data[4][5]['val'] == '20'


    delete_table(uuid, new_token_on_headers)
    data = get_table_data(uuid)
    assert data == {}
