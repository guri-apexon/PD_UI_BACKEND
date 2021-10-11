from fastapi import HTTPException
import pytest
import logging
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient
import json
from fastapi import status
from app.models.pd_user_protocols import PD_User_Protocols
from app.crud.pd_user_protocols import pd_user_protocols
client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")

@pytest.mark.parametrize("file_path",
                         [('app/tests/data/Bulk_Map2.xlsx'),
                          ('app/tests/data/bulk_upload_testing.txt')])
def test_add_user_protocol_many_to_many(file_path):
    bulk_load = pd_user_protocols.excel_data_to_db(db, file_path)
    if bulk_load:
        if file_path == 'app/tests/data/Bulk_Map2.xlsx':
            user_protocol_delete = db.query(PD_User_Protocols).filter(PD_User_Protocols.userId == 'newuser').filter(
                PD_User_Protocols.userId == 'newuser2').filter(PD_User_Protocols.userId == '123456').filter(PD_User_Protocols.userId == 'user3').delete()
            return user_protocol_delete
        assert bulk_load.status == status.HTTP_200_OK

    elif file_path == 'app/tests/data/bulk_upload_testing.txt':
        assert bulk_load == False