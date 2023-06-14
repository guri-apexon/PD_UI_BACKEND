import logging
import uuid

import pytest
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient
from fastapi import status
from app.models.pd_labsparameter_db import IqvlabparameterrecordDb

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")


@pytest.mark.parametrize(
    "doc_id, parameter_text, procedure_panel_text,  assessment, dts, roi_id, "
    "table_link_text, table_sequence_index, table_roi_id ,status_code",
    [
        ("3b44c1d5-f5f7-44ab-901a-3f53c2ba751d", "Lymphocytes", "Haematology/Haemostasis (whole blood)", "Hematology",
         "20230130065337", "b856b6d5-6eff-4600-b821-43fff67e71b9", "Table 7 Laboratory Safety Variables", "-1",
         "49d09a99-02d8-429c-bd3d-bc6978db5301", status.HTTP_200_OK),
        ("3b44c1d5-f5f7-44ab-901a-3f53c2ba751d", "Lymphocytes2", "Haematology/Haemostasis (whole blood)", "Hematology",
         "20230130065337", "b856b6d5-6eff-4600-b821-43fff67e71b9", "Table 7 Laboratory Safety Variables", "sfsd",
         "49d09a99-02d8-429c-bd3d-bc6978db5301", status.HTTP_406_NOT_ACCEPTABLE)
    ]
)
def test_create_labdata(doc_id, parameter_text, procedure_panel_text, assessment, dts, roi_id, table_link_text,
                        table_sequence_index, table_roi_id, status_code, new_token_on_headers):
    create_labdata = client.post("api/lab_data/lab_data_operations", json={
        "data": [{"doc_id": doc_id, "parameter_text": parameter_text, "procedure_panel_text": procedure_panel_text,
                  "assessment": assessment, "dts": dts, "roi_id": roi_id, "table_link_text": table_link_text,
                  "table_roi_id": table_roi_id, "request_type": "create",
                  "table_sequence_index": table_sequence_index}]}, headers=new_token_on_headers)

    assert create_labdata.status_code == status_code
    if create_labdata.status_code == 200:
        assert create_labdata.json()["message"] == "operation completed successfully"


@pytest.mark.parametrize(
    "doc_id, parameter_text, procedure_panel_text,  assessment, dts, roi_id, "
    "table_link_text, table_sequence_index,table_roi_id,status_code",
    [
        (
        "3b44c1d5-f5f7-44ab-901a-3f53c2ba751d", "Lymphocytes3as", "Haematology/Haemostasis (whole blood)", "Hematology",
        "20230130065337", "254e7243-d539-11ed-b74a-005056ab6469", "Table 7 Laboratory Safety Variables", "-1",
        "49d09a99-02d8-429c-bd3d-bc6978db5301", status.HTTP_200_OK)
    ])
def test_update_labdata(doc_id, parameter_text, procedure_panel_text, assessment, dts, roi_id, table_link_text,
                        table_sequence_index, table_roi_id, status_code, new_token_on_headers):
    update_labdata = client.post("api/lab_data/lab_data_operations", json={"data": [
        {"doc_id": doc_id,
         "parameter": "",
         "procedure_panel": "",
         "assessment": assessment,
         "pname": "",
         "ProcessMachineName": "",
         "roi_id": roi_id,
         "table_link_text": table_link_text,
         "table_sequence_index": -1,
         "run_id": "",
         "parameter_text": parameter_text,
         "procedure_panel_text": procedure_panel_text,
         "dts": "20230130065337",
         "ProcessVersion": "",
         "section": "",
         "table_roi_id": table_roi_id,
         "request_type": "update"
         }
    ]}, headers=new_token_on_headers)

    assert update_labdata.status_code == status_code
    if update_labdata.status_code == 200:
        if table_roi_id:
            assert update_labdata.json()["message"] == "operation completed successfully"
        else:
            assert update_labdata.json()["message"] == "operation not completed successfully"


@pytest.mark.parametrize("doc_id, roi_id, table_roi_id, status_code", [
    ("3b44c1d5-f5f7-44ab-901a-3f53c2ba751d", "254e7243-d539-11ed-b74a-005056ab6469",
     "49d09a99-02d8-429c-bd3d-bc6978db5301", status.HTTP_200_OK)
])
def test_delete_labdata(doc_id, roi_id, table_roi_id, status_code, new_token_on_headers):
    delete_labdata = client.post("api/lab_data/lab_data_operations",
                                 json={"data": [{"doc_id": doc_id, "roi_id": roi_id, "table_roi_id": table_roi_id,
                                                 "request_type": "delete"}]},
                                 headers=new_token_on_headers)

    assert delete_labdata.status_code == status_code
    if delete_labdata.status_code == 200:
        if not table_roi_id:
            assert delete_labdata.json().get("message") == "operation not completed successfully"


@pytest.fixture(scope="module")
def lab_data():
    lab_data = {
        "doc_id": "3b44c1d5-f5f7-44ab-901a-3f53c2ba751d",
        "parameter_text": "Lymphocytes",
        "procedure_panel_text": "Haematology/Haemostasis (whole blood)",
        "assessment": "Hematology",
        "dts": "20230130065337",
        "roi_id": 'f717eca9-dd10-11ed-bb40-005056ab6469',
        "table_link_text": "Table 7 Laboratory Safety Variables",
        "table_sequence_index": -1,
        "table_roi_id": "49d09a99-02d8-429c-bd3d-bc6978db5301"
    }
    yield lab_data

    # Clean up created record with roi_id
    roi_id = lab_data.get('roi_id')
    if db.query(IqvlabparameterrecordDb).filter(IqvlabparameterrecordDb.roi_id == roi_id).delete():
        assert True
    else:
        assert False


def test_create_lab_data_table(lab_data, new_token_on_headers):
    create_labdata_table = client.post(
        "api/lab_data/lab_data_table_create",
        json={"data": {"doc_id": lab_data['doc_id']}},
        headers=new_token_on_headers
    )

    assert create_labdata_table.status_code == status.HTTP_200_OK
    assert create_labdata_table.json()[0].get('parameter') is None
    assert create_labdata_table.json()[0].get('doc_id') == lab_data['doc_id']
    assert create_labdata_table.json()[0].get('parameter_text') == 'Lymphocytes'
    assert create_labdata_table.json()[0].get('procedure_panel_text') == 'Haematology/Haemostasis\xa0(whole\xa0blood)'
    assert create_labdata_table.json()[0].get('dts') != ""
    assert create_labdata_table.json()[0].get('ProcessMachineName') is None
    assert create_labdata_table.json()[0].get('roi_id') == lab_data['roi_id']
    assert create_labdata_table.json()[0].get('table_link_text') == "Table 7 Laboratory Safety Variables"
    assert create_labdata_table.json()[0].get('table_sequence_index') == -1
    assert create_labdata_table.json()[0].get('id') != ""
    assert create_labdata_table.json()[0].get('run_id') is None
    assert create_labdata_table.json()[0].get('procedure_panel') is None
    assert create_labdata_table.json()[0].get('assessment') == 'Hematology'
    assert create_labdata_table.json()[0].get('pname') is None
    assert create_labdata_table.json()[0].get('ProcessVersion') is None
    assert create_labdata_table.json()[0].get('section') is None
    assert create_labdata_table.json()[0].get('table_roi_id') == lab_data['table_roi_id']
    assert create_labdata_table.json()[0].get('soft_delete') is None

