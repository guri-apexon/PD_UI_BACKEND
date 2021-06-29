import json
import logging
from datetime import datetime

import pytest
from app import config
from app.db.session import SessionLocal
from app.main import app
from app.models.pd_protocol_metadata import PD_Protocol_Metadata
from fastapi import status
from fastapi.testclient import TestClient

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")


@pytest.mark.parametrize("user_id, protocol, doc_id, dig_status, set_qc_status, expected_flg, comments", [
("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS, config.QcStatus.NOT_STARTED.value, 1, "dig complete, QC not started"),
("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS, config.QcStatus.QC1.value, 1, "dig complete, QC1"),
("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS, config.QcStatus.QC2.value, 1, "dig complete, QC2"),
("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS, config.QcStatus.COMPLETED.value, 1, "dig complete, QC_COMPLETED"),
("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_TRIAGE_STARTED", config.QcStatus.COMPLETED.value, 1, "dig inprogress, QC_COMPLETED"),
("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_TRIAGE_STARTED", config.QcStatus.NOT_STARTED.value, 1, "dig inprogress, QC not started"),
("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "ERROR", config.QcStatus.NOT_STARTED.value, 1, "dig error, QC not started"),
("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "ERROR", config.QcStatus.QC1.value, 1, "dig error, QC1")
])
def test_normal_user(user_id, protocol, doc_id, dig_status, set_qc_status, expected_flg, comments):
    current_timestamp = datetime.utcnow()

    protocol_metadata_doc = db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == doc_id, PD_Protocol_Metadata.isActive == True).first()

    if protocol_metadata_doc:
        protocol_metadata_doc.status = dig_status
        protocol_metadata_doc.qcStatus = set_qc_status
        protocol_metadata_doc.lastUpdated = current_timestamp
        db.merge(protocol_metadata_doc)
        db.commit()
    else:
        logger.error(f"test_normal_user[{comments}]: Could not locate active test file [{doc_id}]")
        assert False

    get_protocols = client.get("/api/protocol_metadata/", params={"userId": user_id})
    assert get_protocols.status_code == status.HTTP_200_OK

    all_curr_user_protocol = json.loads(get_protocols.content)
    if expected_flg:
        assert any([doc['id'] in doc_id for doc in all_curr_user_protocol])
    else:
        assert any([doc['id'] in doc_id for doc in all_curr_user_protocol]) == False

@pytest.mark.parametrize("user_id, protocol, doc_id, dig_status, set_qc_status, expected_flg, comments", [
("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS, config.QcStatus.NOT_STARTED.value, 0, "dig complete, QC not started"),
("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS, config.QcStatus.QC2.value, 0, "dig complete, QC2"),
("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS, config.QcStatus.COMPLETED.value, 0, "dig complete, QC_COMPLETED"),
("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_TRIAGE_STARTED", config.QcStatus.COMPLETED.value, 0, "dig inprogress, QC_COMPLETED"),
("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_TRIAGE_STARTED", config.QcStatus.NOT_STARTED.value, 0, "dig inprogress, QC not started"),
("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "ERROR", config.QcStatus.NOT_STARTED.value, 0, "dig error, QC not started"),
("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "ERROR", config.QcStatus.QC1.value, 0, "dig error, QC1"),
("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_DIG1", config.QcStatus.QC1.value, 0, "dig inprogress, QC1"),
("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS, config.QcStatus.QC1.value, 1, "dig complete, QC1")
])
def test_QC1_user(user_id, protocol, doc_id, dig_status, set_qc_status, expected_flg, comments):
    current_timestamp = datetime.utcnow()

    protocol_metadata_doc = db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == doc_id, PD_Protocol_Metadata.isActive == True).first()

    if protocol_metadata_doc:
        protocol_metadata_doc.status = dig_status
        protocol_metadata_doc.qcStatus = set_qc_status
        protocol_metadata_doc.lastUpdated = current_timestamp
        db.merge(protocol_metadata_doc)
        db.commit()
    else:
        logger.error(f"test_QC1_user[{comments}]: Could not locate active test file [{doc_id}]")
        assert False

    get_protocols = client.get("/api/protocol_metadata/", params={"userId": user_id})
    assert get_protocols.status_code == status.HTTP_200_OK

    all_curr_user_protocol = json.loads(get_protocols.content)
    if expected_flg:
        assert any([doc['id'] in doc_id for doc in all_curr_user_protocol])
    else:
        assert any([doc['id'] in doc_id for doc in all_curr_user_protocol]) == False

@pytest.mark.parametrize("user_id, protocol, doc_id, dig_status, set_qc_status, expected_flg, comments", [
("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS, config.QcStatus.NOT_STARTED.value, 0, "dig complete, QC not started"),
("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS, config.QcStatus.QC1.value, 0, "dig complete, QC1"),
("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS, config.QcStatus.COMPLETED.value, 0, "dig complete, QC_COMPLETED"),
("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_TRIAGE_STARTED", config.QcStatus.COMPLETED.value, 0, "dig inprogress, QC_COMPLETED"),
("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_TRIAGE_STARTED", config.QcStatus.NOT_STARTED.value, 0, "dig inprogress, QC not started"),
("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "ERROR", config.QcStatus.NOT_STARTED.value, 0, "dig error, QC not started"),
("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "ERROR", config.QcStatus.QC2.value, 0, "dig error, QC2"),
("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_DIG1", config.QcStatus.QC2.value, 0, "dig inprogress, QC2"),
("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS, config.QcStatus.QC2.value, 1, "dig complete, QC2")
])
def test_QC2_user(user_id, protocol, doc_id, dig_status, set_qc_status, expected_flg, comments):
    current_timestamp = datetime.utcnow()

    protocol_metadata_doc = db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == doc_id, PD_Protocol_Metadata.isActive == True).first()

    if protocol_metadata_doc:
        protocol_metadata_doc.status = dig_status
        protocol_metadata_doc.qcStatus = set_qc_status
        protocol_metadata_doc.lastUpdated = current_timestamp
        db.merge(protocol_metadata_doc)
        db.commit()
    else:
        logger.error(f"test_QC2_user[{comments}]: Could not locate active test file [{doc_id}]")
        assert False

    get_protocols = client.get("/api/protocol_metadata/", params={"userId": user_id})
    assert get_protocols.status_code == status.HTTP_200_OK

    all_curr_user_protocol = json.loads(get_protocols.content)
    if expected_flg:
        assert any([doc['id'] in doc_id for doc in all_curr_user_protocol])
    else:
        assert any([doc['id'] in doc_id for doc in all_curr_user_protocol]) == False

@pytest.mark.parametrize("user_id, protocol, doc_id, dig_status, set_qc_status, expected_flg, comments", [
("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS, config.QcStatus.NOT_STARTED.value, 1, "dig complete, QC not started"),
("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS, config.QcStatus.QC2.value, 1, "dig complete, QC2"),
("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS, config.QcStatus.COMPLETED.value, 1, "dig complete, QC_COMPLETED"),
("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_TRIAGE_STARTED", config.QcStatus.COMPLETED.value, 1, "dig inprogress, QC_COMPLETED"),
("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_TRIAGE_STARTED", config.QcStatus.NOT_STARTED.value, 1, "dig inprogress, QC not started"),
("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "ERROR", config.QcStatus.NOT_STARTED.value, 1, "dig error, QC not started"),
("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "ERROR", config.QcStatus.QC1.value, 1, "dig error, QC1"),
("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS, config.QcStatus.QC1.value, 1, "dig complete, QC1")
])
def test_single_doc_id(user_id, protocol, doc_id, dig_status, set_qc_status, expected_flg, comments):
    current_timestamp = datetime.utcnow()

    protocol_metadata_doc = db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == doc_id, PD_Protocol_Metadata.isActive == True).first()

    if protocol_metadata_doc:
        protocol_metadata_doc.status = dig_status
        protocol_metadata_doc.qcStatus = set_qc_status
        protocol_metadata_doc.lastUpdated = current_timestamp
        db.merge(protocol_metadata_doc)
        db.commit()
    else:
        logger.error(f"test_single_doc_id[{comments}]: Could not locate active test file [{doc_id}]")
        assert False

    get_protocols = client.get("/api/protocol_metadata/", params={"docId": doc_id})
    assert get_protocols.status_code == status.HTTP_200_OK

    all_curr_user_protocol = json.loads(get_protocols.content)
    if expected_flg:
        assert len(all_curr_user_protocol) == 1
        assert any([doc['id'] in doc_id for doc in all_curr_user_protocol])
    else:
        assert any([doc['id'] in doc_id for doc in all_curr_user_protocol]) == False         
