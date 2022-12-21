import json

import pytest
from app import config
from app.db.session import SessionLocal
from app.main import app
from app.utilities import file_utils
from fastapi import status, UploadFile
from fastapi.testclient import TestClient

client = TestClient(app)
db = SessionLocal()


@pytest.mark.parametrize("aidoc_id, protocol, toc_sensitive_elements, soa_sensitive_elements, attr_sensitive_elements", [
    ("d6c56373-14c3-4474-8219-f1e8d627e8e1", "SSRUT_GEN_002", ("Capivasertib", "Abiraterone"), ("Capivasertib", "Abiraterone"), ("Capivasertib", "Abiraterone"))
])
def test_qc_screen(new_token_on_headers, aidoc_id, protocol, toc_sensitive_elements, soa_sensitive_elements, attr_sensitive_elements):

    # Set proper QC status
    qc_status_resp = client.put("/api/protocol_metadata/change_qc_status", json={"docIdArray": [aidoc_id], "targetStatus": "QC2"}, headers = new_token_on_headers)
    assert qc_status_resp.status_code == status.HTTP_200_OK

    # Get QC data
    qcdata_response = client.get("/api/protocol_qcdata/", params={"id": aidoc_id}, headers=new_token_on_headers)
    assert qcdata_response.status_code == status.HTTP_200_OK

    content = json.loads(qcdata_response.content.decode('utf-8'))
    
    # Basic section check
    assert content['id'] is not None and content['documentFilePath'] is not None 
    assert content['iqvdataToc'] is not None and content['iqvdataSoa'] is not None and content['iqvdataSummary'] is not None
    
    # Redacted string check
    assert config.REDACT_PARAGRAPH_STR not in content['iqvdataToc'] and config.REDACT_PARAGRAPH_STR not in content['iqvdataSoa'] \
            and config.REDACT_ATTR_STR not in content['iqvdataSummary']
    
    # Sensitive elements check
    if toc_sensitive_elements:
        assert all([element in content['iqvdataToc'] for element in toc_sensitive_elements])

    if soa_sensitive_elements:
        assert all([element in content['iqvdataSoa'] for element in soa_sensitive_elements])

    if attr_sensitive_elements:
        assert all([element in content['iqvdataSummary'] for element in attr_sensitive_elements])

    # Verify DB src file
    _, abs_filename = file_utils.get_json_filename(db, aidoc_id=aidoc_id, prefix=config.QC_WIP_SRC_DB_FILE_PREFIX)
    assert abs_filename.is_file()
