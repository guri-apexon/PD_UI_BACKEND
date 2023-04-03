import logging
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
        ("3b44c1d5-f5f7-44ab-901a-3f53c2ba751d", "Lymphocytes", "Haematology/Haemostasis (whole blood)", "Hematology",
         "20230130065337", "b856b6d5-6eff-4600-b821-43fff67e71b9", "Table 7 Laboratory Safety Variables", "",
         "49d09a99-02d8-429c-bd3d-bc6978db5301", status.HTTP_406_NOT_ACCEPTABLE)
    ])
def test_create_labdata(doc_id, parameter_text, procedure_panel_text, assessment, dts, roi_id, table_link_text,
                        table_sequence_index, table_roi_id, status_code, new_token_on_headers):
    create_labdata = client.post("api/lab_data/create_labsparameter", json={
        "data": {"doc_id": doc_id, "parameter_text": parameter_text, "procedure_panel_text": procedure_panel_text,
                 "assessment": assessment, "dts": dts, "roi_id": roi_id, "table_link_text": table_link_text,
                 "table_roi_id": table_roi_id,
                 "table_sequence_index": table_sequence_index}}, headers=new_token_on_headers)
    assert create_labdata.status_code == status_code
    if create_labdata.status_code == 200:
        assert create_labdata.json()['doc_id'] == doc_id


@pytest.mark.parametrize(
    "doc_id, parameter_text, procedure_panel_text,  assessment, dts, roi_id, "
    "table_link_text, table_sequence_index,table_roi_id,status_code",
    [
        ("3b44c1d5-f5f7-44ab-901a-3f53c2ba751d", "Lymphocytes3", "Haematology/Haemostasis (whole blood)", "Hematology",
         "20230130065337", "b856b6d5-6eff-4600-b821-43fff67e71b9", "Table 7 Laboratory Safety Variables", "-1",
         "49d09a99-02d8-429c-bd3d-bc6978db5301", status.HTTP_200_OK)
    ])
def test_update_labdata(doc_id, parameter_text, procedure_panel_text, assessment, dts, roi_id, table_link_text,
                        table_sequence_index, table_roi_id, status_code, new_token_on_headers):
    update_labdata = client.post("api/lab_data/update_labsparameter", json={"data": [
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
         "table_roi_id": table_roi_id
         }
    ]}, headers=new_token_on_headers)

    records = db.query(IqvlabparameterrecordDb).filter(
        IqvlabparameterrecordDb.doc_id == doc_id,
        IqvlabparameterrecordDb.table_roi_id == table_roi_id,
        IqvlabparameterrecordDb.roi_id == roi_id
    ).all()

    assert update_labdata.status_code == status_code

    if update_labdata.status_code == 200:
        assert update_labdata.json() == True

        parameter_text_data = []
        for i in records:
            parameter_text_data.append(i.parameter_text)

        assert True if parameter_text in parameter_text_data else False


@pytest.mark.parametrize("doc_id, roi_id, table_roi_id, status_code", [
    ("3b44c1d5-f5f7-44ab-901a-3f53c2ba751d", "b856b6d5-6eff-4600-b821-43fff67e71b9",
     "49d09a99-02d8-429c-bd3d-bc6978db5301", status.HTTP_200_OK),
    ("3b44c1d5-f5f7-44ab-901a-3f53c2ba751d", "1",
     "1", status.HTTP_406_NOT_ACCEPTABLE)
])
def test_delete_labdata(doc_id, roi_id, table_roi_id, status_code, new_token_on_headers):
    delete_labdata = client.post("api/lab_data/delete_labsparameter",
                                 json={"data": {"doc_id": doc_id, "roi_id": roi_id, "table_roi_id": table_roi_id}},
                                 headers=new_token_on_headers)

    assert delete_labdata.status_code == status_code

    all_records = db.query(IqvlabparameterrecordDb).filter(
        IqvlabparameterrecordDb.doc_id == doc_id,
        IqvlabparameterrecordDb.table_roi_id == table_roi_id,
        IqvlabparameterrecordDb.roi_id == roi_id
    )
    for i in all_records:
        assert i.soft_delete == True

    all_records.delete()
    db.commit()
