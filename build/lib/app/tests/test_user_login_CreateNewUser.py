import logging
import pytest
from app.db.session import SessionLocal
from app.main import app
from app.models.pd_login import Login
from app.models.pd_user import User
from fastapi import status
from fastapi.testclient import TestClient

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")


@pytest.mark.parametrize("insert_flag, username, first_name,last_name,email,country,user_type, expected_response",
                         [("0", "class101", "CS", "IT", "cs.it@iqvia.com", "USA", "normal", status.HTTP_409_CONFLICT),
                          ("1", "casio", "Casio", "Watch Brand IN", "casio.watchbrand@iqvia.com", "India", "normal", status.HTTP_200_OK),
                          ("0", "newclass", "", "new", "", "India", "", status.HTTP_422_UNPROCESSABLE_ENTITY)
                          ])
def test_create_add_new_user(insert_flag, username, first_name, last_name, email, country,  user_type, expected_response, new_token_on_headers):
    if insert_flag == "1":
        user_delete = db.query(User).filter(User.username == "casio").delete()
        login_delete = db.query(Login).filter(Login.username == "casio").delete()
        return user_delete and login_delete
    create_user_in_login_user = client.post("api/create_new_user/new_user",
                                            json={"username": username, "first_name": first_name,
                                                  "last_name": last_name, "email": email, "country": country,
                                                  "user_type": user_type}, headers=new_token_on_headers)
    assert create_user_in_login_user.status_code == expected_response
