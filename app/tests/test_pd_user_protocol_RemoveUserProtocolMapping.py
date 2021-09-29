from fastapi import HTTPException
import pytest
import logging
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient
import json
from fastapi import status
from app.models.pd_user_protocols import PD_User_Protocols

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")

@pytest.mark.parametrize("userId, protocol, isActive, expected_response",[("class101","css", False, status.HTTP_200_OK),
                                                                          ("class201","cs",False, status.HTTP_403_FORBIDDEN),
                                                                          ("asdf","wer", False, status.HTTP_403_FORBIDDEN)])
def test_soft_delete(userId, protocol, isActive, expected_response, new_token_on_headers):
    soft_delete_user_protocol = client.put("api/user_protocol/delete_userprotocol", json={"userId":userId,
                                                                                          "protocol":protocol,
                                                                                          "isActive":isActive,
                                                                                          }, headers=new_token_on_headers)
    if soft_delete_user_protocol.status_code == expected_response:
        if expected_response == status.HTTP_200_OK:
            user_protocol_delete = db.query(PD_User_Protocols).filter(PD_User_Protocols.userId == userId,
                                                                          PD_User_Protocols.protocol == protocol).first()
            isActive = user_protocol_delete.isActive
            user_protocol_delete.isActive = True
            db.add(user_protocol_delete)
            db.commit()
            assert isActive == False

        elif expected_response == status.HTTP_403_FORBIDDEN:
            assert True
    else:
        assert False