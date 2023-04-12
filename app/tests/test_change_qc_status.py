import json
import logging
from datetime import datetime

import pytest
from app import config
from app.db.session import SessionLocal
from app.main import app
from app.models.pd_protocol_metadata import PD_Protocol_Metadata
from app.models.pd_protocol_qc_summary_data import PDProtocolQCSummaryData
from app.utilities import file_utils
from fastapi import status
from fastapi.testclient import TestClient
from app import crud

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")

@pytest.mark.parametrize("user_id, protocol, doc_id_1, doc_id_2, set_qc_status, expected_response,  comments", [
("1034911", "SSRUT_GEN_00?", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "263b3fec-07c6-4ab1-8099-230a0988f7e1", "QC1", status.HTTP_200_OK, "Change to QC1"),
("1034911", "SSRUT_GEN_00?", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "263b3fec-07c6-4ab1-8099-230a0988f7e1", "QC2", status.HTTP_200_OK, "Change to QC2"),
("1034911", "SSRUT_GEN_00?", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "263b3fec-07c6-4ab1-8099-230a0988f7e1", "QC_NOT_STARTED", status.HTTP_200_OK, "Change to QC_NOT_STARTED"),
("1034911", "SSRUT_GEN_00?", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "263b3fec-07c6-4ab1-8099-230a0988f7e1", "QC", status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid QC status1"),
("1034911", "SSRUT_GEN_00?", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "263b3fec-07c6-4ab1-8099-230a0988f7e1", "QC_COMPLETED", status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid QC status2")
])
def test_qc1_qc_notstarted(new_token_on_headers, user_id, protocol, doc_id_1, doc_id_2,  set_qc_status, expected_response, comments):
    doc_id_array = [doc_id_1, doc_id_2]
    qc_status_resp = client.put("/api/protocol_metadata/change_qc_status", json={"docIdArray": doc_id_array, "targetStatus": set_qc_status}, headers = new_token_on_headers)
    assert qc_status_resp.status_code == expected_response

    if expected_response == status.HTTP_200_OK:
        protocol_metadata_doc_1 = db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == doc_id_1, PD_Protocol_Metadata.isActive == True).first()
        protocol_metadata_doc_2 = db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == doc_id_2, PD_Protocol_Metadata.isActive == True).first()
        
        if protocol_metadata_doc_1 and protocol_metadata_doc_2:
            assert protocol_metadata_doc_1.qcStatus == set_qc_status
            assert protocol_metadata_doc_2.qcStatus == set_qc_status
        else:
            logger.error(f"test_changeqc[{comments}]: Could not locate active test file [{doc_id_1} or {doc_id_2}] of {user_id}/{protocol}")
            assert False

@pytest.mark.parametrize("doc_id, qc_status, response, comments", [
("17e79287-ca4c-47aa-821a-21268ee0dc42", "QC_COMPLETED", True,"doc id exists and change status"),
("17e79287-ca4c-47aa-821a-21268ee0dc42", "TEST_STATUS", True,"doc id with different status"),
("17e79287-ca4c-47aa-821a-21268ee0dc42no", "QC_COMPLETED", False, "doc id does not exists"),
])
def test_qcapproved(new_token_on_headers, doc_id, qc_status, response, comments):

    # updating status to TEST_STATUS
    _ , _ = crud.pd_protocol_metadata.change_status(db, doc_id, qc_status)
    metadata_resource = crud.pd_protocol_metadata.get_by_id(db, id = doc_id)
    if metadata_resource:
        assert metadata_resource.status == qc_status

    qc_status_resp = client.put("/api/protocol_metadata/qc_approve", params={"aidoc_id": doc_id}, headers = new_token_on_headers)
    if qc_status_resp.status_code == status.HTTP_200_OK:
        assert qc_status_resp.json() == response
        if qc_status_resp.json():
            db.refresh(metadata_resource)
            assert crud.pd_protocol_metadata.get_by_id(db, id = doc_id).status == config.QC_COMPLETED_STATUS
    else:
        assert False
