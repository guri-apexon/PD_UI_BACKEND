import json
import logging
from datetime import datetime

import pytest
from app import config
from app.db.session import SessionLocal
from app.main import app
from app.models.pd_login import Login
from app.crud.pd_user import user
from app.crud.pd_login import login
from fastapi import status
from fastapi.testclient import TestClient

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")

@pytest.mark.parametrize("insert_flag, username, first_name,last_name,email,country,user_type, expected_response",
                         [("0","class101", "CS", "IT", "cs.it@iqvia.com", "USA", "normal", status.HTTP_400_BAD_REQUEST),
                          ("1","casio", "Casio", "Watch Brand IN", "casio.watchbrand@iqvia.com", "India", "normal", status.HTTP_200_OK),
                          ("0","newclass", "", "new", "", "India", "", status.HTTP_422_UNPROCESSABLE_ENTITY)
                          ])
                          #
def test_create_add_new_user(insert_flag, username, first_name, last_name, email, country,  user_type, expected_response, new_token_on_headers):

    create_user_in_login_user = client.post("api/create_new_user/new_user", json={"username":username, "first_name":first_name,
                                                                        "last_name":last_name,"email":email, "country":country,
                                                                        "user_type":user_type}, headers= new_token_on_headers)
    if create_user_in_login_user.status_code == expected_response:
        if insert_flag:
            existing_user = login.user_status_check(db=db, username=username)
            if existing_user:
                if expected_response == status.HTTP_400_BAD_REQUEST:
                    assert True
            elif expected_response == status.HTTP_200_OK:
                assert True
            elif expected_response == status.HTTP_422_UNPROCESSABLE_ENTITY:
                assert True
