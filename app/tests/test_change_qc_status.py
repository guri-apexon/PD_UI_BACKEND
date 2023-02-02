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

@pytest.mark.parametrize("user_id, protocol, doc_id, approver_id, expected_response,  comments", [
("1034911", "SSRUT_GEN_00?", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "1034911", status.HTTP_200_OK, "QC approved"),
("1034911", "SSRUT_GEN_00?", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf", "1034911", status.HTTP_403_FORBIDDEN, "QC approved - failure case")
])
def test_qcapproved(new_token_on_headers, user_id, protocol, doc_id,  approver_id, expected_response, comments):
    current_timestamp = datetime.utcnow()

    # Rename file
    _, _ = file_utils.rename_json_file(db, aidoc_id = doc_id, src_prefix=config.QC_APPROVED_FILE_PREFIX, target_prefix=config.QC_WIP_SRC_DB_FILE_PREFIX, feedback_flag=True)

    # Approve
    qc_status_resp = client.put("/api/protocol_metadata/qc_approve", params={"aidoc_id": doc_id, "approvedBy": approver_id}, headers = new_token_on_headers)
    assert qc_status_resp.status_code == expected_response

    if expected_response == status.HTTP_200_OK:
        # Verify qc status
        protocol_metadata_doc = db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == doc_id, PD_Protocol_Metadata.isActive == True).first()
        
        if protocol_metadata_doc:
            assert protocol_metadata_doc.qcStatus == config.QC_APPROVED_STATUS
        else:
            logger.error(f"test_qcapproved[{comments}]: Could not locate active test file [{doc_id}] of {user_id}/{protocol}")
            assert False

        # Verify data
        protocol_qc_summ_data_doc_id = db.query(PDProtocolQCSummaryData.aidocId, PDProtocolQCSummaryData.qcApprovedBy, PDProtocolQCSummaryData.timeUpdated)\
                                                .filter(PDProtocolQCSummaryData.aidocId == doc_id, PDProtocolQCSummaryData.source == 'QC').first()
        
        if protocol_qc_summ_data_doc_id:
            assert protocol_qc_summ_data_doc_id.timeUpdated >= current_timestamp
            assert protocol_qc_summ_data_doc_id.qcApprovedBy == approver_id
        else:
            logger.error(f"test_qcapproved[{comments}]: Could not locate SRC record in  [{doc_id}] of {user_id}/{protocol}")
            assert False

        # Verify QC file
        _, abs_filename = file_utils.get_json_filename(db, aidoc_id=doc_id, prefix=config.QC_APPROVED_FILE_PREFIX, feedback_flag=True)
        assert abs_filename.is_file()
