import logging
import pytest
import json
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")


@pytest.mark.parametrize("qc_ingest_test_data", [(r"./app/tests/data/qc_ingest_test_data.json")])
def test_document_header(new_token_on_headers, qc_ingest_test_data):
    """
        Tests QC Ingest.
    """
    with open(qc_ingest_test_data, 'r') as f:
        data = f.read()
        qc_ingest_test_data_json = json.loads(data)
    get_qc_ingest = client.post(
        "/api/qc_ingest/", json=qc_ingest_test_data_json, headers=new_token_on_headers)
    assert get_qc_ingest.status_code == 200
