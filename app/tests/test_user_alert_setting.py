import json

import pytest
from app.models.pd_user import User
from datetime import datetime

from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient
from fastapi import status

client = TestClient(app)
db = SessionLocal()


def create_user_alert_setting_record():
    user_id = '1234567_test'
    alert_obj = db.query(User).filter(User.username == user_id).first()
    if not alert_obj:
        alert_obj = User(first_name='Dev_test',
                         last_name='Dev_test',
                         country='IN',
                         email='dev_test@example.com',
                         username=user_id,
                         user_type='primary',
                         qc_complete=True,
                         new_document_version=True,
                         edited=True)
        try:
            db.add(alert_obj)
            db.commit()
            db.refresh(alert_obj)
        except Exception as ex:
            db.rollback()


@pytest.mark.parametrize("user_id, status_code, result", [
    ("1234567_test", status.HTTP_200_OK,
     {"QC_Complete": True, "New_Document/Version": True, "Edited": True}),
    ("1234589_test", status.HTTP_200_OK, False)
])
def test_get_user_alert_setting(new_token_on_headers, user_id, status_code,
                                result):
    """
    To verify get call to check user alert setting options
    """
    # To create record if not exist
    create_user_alert_setting_record()
    user_setting = client.get("api/user_alert_setting/",
                              params={"user_id": user_id},
                              headers=new_token_on_headers)
    assert user_setting.status_code == status_code
    response = json.loads(user_setting.text)
    if response:
        assert response.get('options') == result
    else:
        assert response == result


@pytest.mark.parametrize("user_id, payload, status_code, result", [
    ("1234567_test",
     {"QC_Complete": False, "New_Document/Version": True, "Edited": True},
     status.HTTP_200_OK,
     {"QC_Complete": False, "New_Document/Version": True, "Edited": True}),
    ("1234567_test", {}, status.HTTP_200_OK,
     {"QC_Complete": False, "New_Document/Version": False, "Edited": False}),
    ("1234567_test",
     {"QC_Complete": True, "New_Document/Version": True, "Edited": True},
     status.HTTP_200_OK,
     {"QC_Complete": True, "New_Document/Version": True, "Edited": True}),
    ("1234589_test", {}, status.HTTP_200_OK, False)
])
def test_update_user_alert_setting(new_token_on_headers, user_id, payload,
                                   status_code, result):
    """
    To verify updated user setting options
    """
    # To create record if not exist
    create_user_alert_setting_record()
    user_setting = client.post("api/user_alert_setting/update_setting/",
                               json={"data": {"userId": user_id,
                                              "options": payload}},
                               headers=new_token_on_headers)
    assert user_setting.status_code == status_code
    response = json.loads(user_setting.text)
    if response:
        assert response.get('options') == result
    else:
        assert response == result
