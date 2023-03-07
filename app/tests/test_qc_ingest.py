import logging
import pytest
import json
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")


@pytest.mark.parametrize("qc_ingest_test_data",[(r"./app/tests/data/qc_ingest_text_curd_data.json") ])
def test_document_line_curd(new_token_on_headers, qc_ingest_test_data):
    """
        create,update,delete line
    """
    with open(qc_ingest_test_data, 'r') as f:
        data = f.read()
        test_payload_list = json.loads(data)
    for payload in test_payload_list:
        get_qc_ingest = client.post(
            "/api/qc_ingest/", json=[payload], headers=new_token_on_headers)
        assert get_qc_ingest.status_code == 200

@pytest.mark.parametrize("qc_ingest_test_data", [(r"./app/tests/data/qc_ingest_image_curd_data.json")])
def test_document_image_curd(new_token_on_headers, qc_ingest_test_data):
    """
 
    SELECT * FROM public.iqvdocumentimagebinary_db WHERE "para_id"='mnf5d19t-16f5-4xf2-xe06-35fcc0c0eeux'
    """
    with open(qc_ingest_test_data, 'r') as f:
        data = f.read()
        test_payload_list = json.loads(data)
    for payload in test_payload_list:
        get_qc_ingest = client.post(
            "/api/qc_ingest/", json=[payload], headers=new_token_on_headers)
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
    with open(qc_ingest_test_data, 'r') as f:
        data = f.read()
        test_payload_list = json.loads(data)
    for payload in test_payload_list:
        get_qc_ingest = client.post(
            "/api/qc_ingest/", json=[payload], headers=new_token_on_headers)
        assert get_qc_ingest.status_code == 200





