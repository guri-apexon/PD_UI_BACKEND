from fastapi import HTTPException
import pytest
from app.api.endpoints import pd_user_get_all_active_users
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient
import json
from fastapi import status
from app.models.pd_user import User


client = TestClient(app)
db = SessionLocal()

@pytest.mark.parametrize("userId, test_setup_flag",
                         [("1063396", True),
                          ("q1020640", True),
                          ("q814693", False),
                          (None, False)
                          ])
def test_get_all_user(new_token_on_headers, userId, test_setup_flag):

    response = client.get("/api/user/read_all_users", params={"userId": userId}, headers=new_token_on_headers)
    if response.status_code == 200:
        if userId is None:
            assert len(response.json()) > 0
        else:
            res_json = response.json()
            if test_setup_flag:
                assert res_json and userId in res_json['username']
            else:
                assert res_json is None
    else:
        assert False
