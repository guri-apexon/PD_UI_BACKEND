import pytest
from app import crud, schemas
from app.main import app
from fastapi.testclient import TestClient
from app.db.session import SessionLocal
from app.models.pd_protocol_qcdata import PD_Protocol_QCData
import time
from app.utilities.elastic_utilities import get_elastic_doc_by_id, update_elastic
from http import HTTPStatus
from app import config


client = TestClient(app)

@pytest.mark.parametrize(
    ["aidocid", "qc_status", "insert_flag"],
    [
        ('171ef754-2a33-4c8d-8a90-009941ddbba0', config.QcStatus.QC1.value, 1),
        ('171ef754-2a33-4c8d-8a90-009941ddb', config.QcStatus.QC1.value, 0)

     ])
def test_query_elastic(aidocid, qc_status, insert_flag):

    db = SessionLocal()

    response = crud.qc_update_elastic(aidocid, db, qc_status=qc_status)
    if insert_flag:
        es_data = get_elastic_doc_by_id(aidocid)
        if es_data:
            assert response['ResponseCode'] == HTTPStatus.OK and es_data['_source'].get('QC_Flag', '') == True
            assert es_data['_source'].get('qcStatus', '') == qc_status
            es_dict = dict()
            es_dict['QC_Flag'] = False
            update_elastic({'doc': es_dict}, aidocid)
        else:
            assert False
    elif insert_flag == False:
        es_data = get_elastic_doc_by_id(aidocid)
        if es_data:
            assert False
        else:
            assert True
