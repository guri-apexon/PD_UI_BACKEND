from fastapi import HTTPException
import pytest
import logging
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient
import json
from fastapi import status
from app.models.pd_user import User
from app.models.pd_login import Login


client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")

@pytest.mark.parametrize("username, first_name, last_name, email, country, user_type, expected_response",
                         [("casio", "Casio", "Watch Brand IN", "casio.watchbrand@iqvia.com", "India", "normal", status.HTTP_200_OK),
                          ("f2","foo","panda","foo.panda@iqvia.com","India","normal", status.HTTP_404_NOT_FOUND)])
def test_update(username, first_name, last_name, email, country,  user_type, expected_response, new_token_on_headers):
    previous_details = db.query(User).filter(User.username == username, User.first_name==first_name, User.last_name==last_name,
                                             User.email == email, User.country==country, User.user_type==user_type).first()
    user_update = client.put("/api/user_login/update_existing",
                             json={"username": username, "first_name": first_name, "last_name": last_name,
                                                                  "email": email, "country": country,
                                                                  "user_type": user_type}, headers=new_token_on_headers)
    if user_update.status_code == expected_response:
        if expected_response == status.HTTP_200_OK:
            userin = db.query(User).filter(User.username == username).first()

            if previous_details.username == userin.username:
                if first_name != "":
                    assert userin.first_name != "" and userin.first_name == first_name
                else:
                    assert userin.first_name != "" and userin.first_name == previous_details.first_name
                if last_name != "":
                    assert userin.last_name != "" and userin.last_name == last_name
                else:
                    assert userin.last_name != "" and userin.last_name == previous_details.last_name
                if email != "":
                    assert userin.email != "" and userin.email == email
                else:
                    assert userin.email != "" and userin.email == previous_details.email
                if country != "":
                    assert userin.country != "" and userin.country == country
                else:
                    assert userin.country != "" and userin.country == previous_details.country
                if user_type != "":
                    assert userin.user_type != "" and userin.user_type == user_type
                else:
                    assert userin.user_type != "" and userin.user_type == previous_details.user_type
        elif expected_response == status.HTTP_404_NOT_FOUND:
            assert True
        else:
            assert False

    else:
        assert False

@pytest.mark.parametrize("username, active_user, expected_response",[("usetesting", False, status.HTTP_200_OK),
                                                                       ("class101", False, status.HTTP_200_OK),
                                                                     ("f2", False, status.HTTP_404_NOT_FOUND)])
def test_soft_delete(username, active_user, expected_response, new_token_on_headers):

    soft_delete_user = client.put("/api/user_login/delete_user", json={"username":username,
                                                                           "active_user":active_user
                                                                           }, headers=new_token_on_headers)
    if soft_delete_user.status_code == expected_response:
        if expected_response == status.HTTP_200_OK:
            login_delete = db.query(Login).filter(Login.username == username).first()
            assert login_delete.active_user == False
            login_delete.active_user = True
            db.add(login_delete)
            db.commit()
        elif expected_response == status.HTTP_404_NOT_FOUND:
            assert True
        else:
            assert False
    else:
        assert False
