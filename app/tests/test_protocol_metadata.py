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


@pytest.mark.parametrize(
    "user_id, protocol, doc_id, dig_status, set_qc_status, set_follow_flg, userUploadedFlag, userPrimaryRoleFlag, userFollowingFlag,  expected_flg,  comments",
    [
        ("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS,
         config.QcStatus.NOT_STARTED.value, False, True, False, False, 1, "dig complete, QC not started"),
        ("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS,
         config.QcStatus.QC1.value, False, True, False, False, 1, "dig complete, QC1"),
        ("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS,
         config.QcStatus.QC2.value, False, True, False, False, 1, "dig complete, QC2"),
        ("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS,
         config.QcStatus.COMPLETED.value, False, True, False, False, 1, "dig complete, QC_COMPLETED"),
        ("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_TRIAGE_STARTED",
         config.QcStatus.COMPLETED.value, False, True, False, False, 1, "dig inprogress, QC_COMPLETED"),
        ("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_TRIAGE_STARTED",
         config.QcStatus.NOT_STARTED.value, False, True, False, False, 1, "dig inprogress, QC not started"),
        ("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "ERROR", config.QcStatus.NOT_STARTED.value,
         False, True, False, False, 1, "dig error, QC not started"),
        ("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "ERROR", config.QcStatus.QC1.value, False,
         True, False, False, 1, "dig error, QC1"),
        ("1034911", "SSRUT_GEN_002", "263b3fec-07c6-4ab1-8099-230a0988f7e1", config.DIGITIZATION_COMPLETED_STATUS,
         config.QcStatus.NOT_STARTED.value, True, False, False, True, 1, "Following other protocol"),
        ("1034911", "SSRUT_GEN_002", "263b3fec-07c6-4ab1-8099-230a0988f7e1", config.DIGITIZATION_COMPLETED_STATUS,
         config.QcStatus.NOT_STARTED.value, False, False, False, False, 0, "Stopped following other protocol"),
        ("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS,
         config.QcStatus.QC1.value, False, True, False, False, 1, "Unfollow my own protocol"),
        ("1034911", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS,
         config.QcStatus.QC1.value, True, True, False, True, 1, "Follow my own protocol")
    ])
def test_normal_user(new_token_on_headers, user_id, protocol, doc_id, dig_status, set_qc_status, set_follow_flg,
                     userUploadedFlag, userPrimaryRoleFlag, userFollowingFlag, expected_flg, comments):
    current_timestamp = datetime.utcnow()

    protocol_metadata_doc = db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == doc_id,
                                                                  PD_Protocol_Metadata.isActive == True).first()

    if protocol_metadata_doc:
        protocol_metadata_doc.status = dig_status
        protocol_metadata_doc.qcStatus = set_qc_status
        protocol_metadata_doc.lastUpdated = current_timestamp
        db.merge(protocol_metadata_doc)
        db.commit()
    else:
        logger.error(f"test_normal_user[{comments}]: Could not locate active test file [{doc_id}]")
        assert False

    # Set follow flag
    follow_response = client.post("/api/follow_protocol/",
                                  json={"userId": user_id, "protocol": protocol, "follow": set_follow_flg,
                                        "userRole": config.FOLLOW_DEFAULT_ROLE}, headers=new_token_on_headers)
    assert follow_response.status_code == 200

    get_protocols = client.get("/api/protocol_metadata/", params={"userId": user_id}, headers=new_token_on_headers)

    assert get_protocols.status_code == status.HTTP_200_OK

    all_curr_user_protocol = json.loads(get_protocols.content)
    exp_doc_list = [doc for doc in all_curr_user_protocol if doc['id'] in doc_id]
    len_exp_doc_list = len(exp_doc_list)
    exp_doc = exp_doc_list[0] if len_exp_doc_list > 0 else None

    # My protocols
    if expected_flg:
        assert len_exp_doc_list > 0
        assert exp_doc['userUploadedFlag'] == userUploadedFlag  # Following protocols
        assert exp_doc['userPrimaryRoleFlag'] == userPrimaryRoleFlag
        assert exp_doc['userFollowingFlag'] == userFollowingFlag
    else:
        assert len_exp_doc_list == 0


@pytest.mark.parametrize("user_id, protocol, doc_id, dig_status, set_qc_status, expected_flg, comments", [
    ("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS,
     config.QcStatus.NOT_STARTED.value, 0, "dig complete, QC not started"),
    ("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS,
     config.QcStatus.QC2.value, 0, "dig complete, QC2"),
    ("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS,
     config.QcStatus.COMPLETED.value, 0, "dig complete, QC_COMPLETED"),
    ("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_TRIAGE_STARTED",
     config.QcStatus.COMPLETED.value, 0, "dig inprogress, QC_COMPLETED"),
    ("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_TRIAGE_STARTED",
     config.QcStatus.NOT_STARTED.value, 0, "dig inprogress, QC not started"),
    ("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "ERROR", config.QcStatus.NOT_STARTED.value, 0,
     "dig error, QC not started"),
    ("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "ERROR", config.QcStatus.QC1.value, 0,
     "dig error, QC1"),
    ("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_DIG1", config.QcStatus.QC1.value, 0,
     "dig inprogress, QC1"),
    ("QC1", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS,
     config.QcStatus.QC1.value, 1, "dig complete, QC1")
])
def test_QC1_user(new_token_on_headers, user_id, protocol, doc_id, dig_status, set_qc_status, expected_flg, comments):
    current_timestamp = datetime.utcnow()

    protocol_metadata_doc = db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == doc_id,
                                                                  PD_Protocol_Metadata.isActive == True).first()

    if protocol_metadata_doc:
        protocol_metadata_doc.status = dig_status
        protocol_metadata_doc.qcStatus = set_qc_status
        protocol_metadata_doc.lastUpdated = current_timestamp
        db.merge(protocol_metadata_doc)
        db.commit()
    else:
        logger.error(f"test_QC1_user[{comments}]: Could not locate active test file [{doc_id}]")
        assert False

    get_protocols = client.get("/api/protocol_metadata/", params={"userId": user_id}, headers=new_token_on_headers)
    assert get_protocols.status_code == status.HTTP_200_OK

    all_curr_user_protocol = json.loads(get_protocols.content)
    if expected_flg:
        assert any([doc['id'] in doc_id for doc in all_curr_user_protocol])
    else:
        assert any([doc['id'] in doc_id for doc in all_curr_user_protocol]) == False


@pytest.mark.parametrize("user_id, protocol, doc_id, dig_status, set_qc_status, expected_flg, comments", [
    ("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS,
     config.QcStatus.NOT_STARTED.value, 0, "dig complete, QC not started"),
    ("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS,
     config.QcStatus.QC1.value, 0, "dig complete, QC1"),
    ("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS,
     config.QcStatus.COMPLETED.value, 0, "dig complete, QC_COMPLETED"),
    ("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_TRIAGE_STARTED",
     config.QcStatus.COMPLETED.value, 0, "dig inprogress, QC_COMPLETED"),
    ("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_TRIAGE_STARTED",
     config.QcStatus.NOT_STARTED.value, 0, "dig inprogress, QC not started"),
    ("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "ERROR", config.QcStatus.NOT_STARTED.value, 0,
     "dig error, QC not started"),
    ("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "ERROR", config.QcStatus.QC2.value, 0,
     "dig error, QC2"),
    ("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", "UT_DIG1", config.QcStatus.QC2.value, 0,
     "dig inprogress, QC2"),
    ("QC2", "SSRUT_GEN_001", "5c59dbc6-bacc-49d9-a9c6-0a43fa96bf0a", config.DIGITIZATION_COMPLETED_STATUS,
     config.QcStatus.QC2.value, 1, "dig complete, QC2")
])
def test_QC2_user(new_token_on_headers, user_id, protocol, doc_id, dig_status, set_qc_status, expected_flg, comments):
    current_timestamp = datetime.utcnow()

    protocol_metadata_doc = db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == doc_id,
                                                                  PD_Protocol_Metadata.isActive == True).first()

    if protocol_metadata_doc:
        protocol_metadata_doc.status = dig_status
        protocol_metadata_doc.qcStatus = set_qc_status
        protocol_metadata_doc.lastUpdated = current_timestamp
        db.merge(protocol_metadata_doc)
        db.commit()
    else:
        logger.error(f"test_QC2_user[{comments}]: Could not locate active test file [{doc_id}]")
        assert False

    get_protocols = client.get("/api/protocol_metadata/", params={"userId": user_id}, headers=new_token_on_headers)
    assert get_protocols.status_code == status.HTTP_200_OK

    all_curr_user_protocol = json.loads(get_protocols.content)
    if expected_flg:
        assert any([doc['id'] in doc_id for doc in all_curr_user_protocol])
        for doc in all_curr_user_protocol:
            if doc['redactProfile'] in ['profile_0']:
                assert config.REDACT_PARAGRAPH_STR in doc.values()
    else:
        assert any([doc['id'] in doc_id for doc in all_curr_user_protocol]) == False


@pytest.mark.parametrize("user_id, protocol, doc_id, dig_status, set_qc_status, expected_flg, comments", [
    ("1036048", "AKB-6548-CI-0014", "65199ae2-960c-4b6b-ada3-409b3d7990af", config.DIGITIZATION_COMPLETED_STATUS,
     config.QcStatus.NOT_STARTED.value, 1, "dig complete, QC not started"),
    ("1036048", "AKB-6548-CI-0014", "65199ae2-960c-4b6b-ada3-409b3d7990af", config.DIGITIZATION_COMPLETED_STATUS,
     config.QcStatus.QC2.value, 1, "dig complete, QC2"),
    ("1036048", "AKB-6548-CI-0014", "65199ae2-960c-4b6b-ada3-409b3d7990af", config.DIGITIZATION_COMPLETED_STATUS,
     config.QcStatus.COMPLETED.value, 1, "dig complete, QC_COMPLETED"),
    ("1036048", "AKB-6548-CI-0014", "65199ae2-960c-4b6b-ada3-409b3d7990af", "UT_TRIAGE_STARTED",
     config.QcStatus.COMPLETED.value, 1, "dig inprogress, QC_COMPLETED"),
    ("1036048", "AKB-6548-CI-0014", "65199ae2-960c-4b6b-ada3-409b3d7990af", "UT_TRIAGE_STARTED",
     config.QcStatus.NOT_STARTED.value, 1, "dig inprogress, QC not started"),
    ("1036048", "AKB-6548-CI-0014", "65199ae2-960c-4b6b-ada3-409b3d7990af", "ERROR", config.QcStatus.NOT_STARTED.value,
     1, "dig error, QC not started"),
    ("1036048", "AKB-6548-CI-0014", "65199ae2-960c-4b6b-ada3-409b3d7990af", "ERROR", config.QcStatus.QC1.value, 1,
     "dig error, QC1"),
    ("1036048", "AKB-6548-CI-0014", "65199ae2-960c-4b6b-ada3-409b3d7990af", config.DIGITIZATION_COMPLETED_STATUS,
     config.QcStatus.QC1.value, 1, "dig complete, QC1"),
    ("1036048", "AKB-6548-CI-0014", "5c59dbc6-bacc-49d9-a9c6-0a43fa96b", config.DIGITIZATION_COMPLETED_STATUS,
     config.QcStatus.QC1.value, 0, "Document not present")
])
def test_single_doc_id(new_token_on_headers, user_id, protocol, doc_id, dig_status, set_qc_status, expected_flg,
                       comments):
    current_timestamp = datetime.utcnow()

    protocol_metadata_doc = db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == doc_id,
                                                                  PD_Protocol_Metadata.isActive == True).first()

    if protocol_metadata_doc:
        protocol_metadata_doc.status = dig_status
        protocol_metadata_doc.qcStatus = set_qc_status
        protocol_metadata_doc.lastUpdated = current_timestamp
        db.merge(protocol_metadata_doc)
        db.commit()
    elif expected_flg:
        logger.error(f"test_single_doc_id[{comments}]: Could not locate active test file [{doc_id}]")
        assert False
    else:
        assert True
        return

    get_protocols = client.get("/api/protocol_metadata/", params={"docId": doc_id}, headers=new_token_on_headers)
    assert get_protocols.status_code == status.HTTP_200_OK

    all_curr_user_protocol = json.loads(get_protocols.content)
    if expected_flg:
        assert len(all_curr_user_protocol) == 1
        assert any([doc['id'] in doc_id for doc in all_curr_user_protocol])
        if all_curr_user_protocol[0]['redactProfile'] in [None, 'profile_0']:
            assert config.REDACT_PARAGRAPH_STR in all_curr_user_protocol[0].values()
    else:
        assert any([doc['id'] in doc_id for doc in all_curr_user_protocol]) == False
