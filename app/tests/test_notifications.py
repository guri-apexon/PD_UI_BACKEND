import logging
from fastapi import status
import pytest
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient

from app.models.pd_protocol_alert import ProtocolAlert

client = TestClient(app)
db = SessionLocal()
logger = logging.getLogger("unit-test")


@pytest.mark.parametrize("user_id, status, comments", [
    ('1139339', True, "valid user id and retrieved notifications if not read"),
    ('1149473_not_valid', False,
     "in valid user id and retrieved empty notifications"),

])
def test_get_notifications(new_token_on_headers, user_id, status, comments):
    """
        Tests PD Notificaitons get based on user_id.
    """
    get_notifications = client.get("/api/pd_notification/", params={
        "user_id": user_id}, headers=new_token_on_headers)

    assert bool(get_notifications.json()) == status


@pytest.mark.parametrize("aidocId, id, protocol, action, status, comments", [
    ("fd9e2b93-bdb1-4ecd-83ef-d88ac979569d", "21678", "I1F-MC-RHBE(a)", "read",
     200, "notification is read"),
    (
    "fd9e2b93-bdb1-4ecd-83ef-d88ac979569d", "21678", "I1F-MC-RHBE(a)", "delete",
    200, "notification is removed(soft deleted)"),
])
def test_update_notification_read_record(new_token_on_headers, aidocId, id,
                                         protocol, action, status, comments):
    """
        update readflag if user read notification
        update isactive flag if user removed notification
    """

    try:
        # making record to active later inactive and verify response
        if action == "delete":
            db.query(ProtocolAlert).filter(ProtocolAlert.id == id,
                                           ProtocolAlert.protocol == protocol,
                                           ProtocolAlert.aidocId == aidocId).update(
                {ProtocolAlert.isActive: True})
        elif action == "read":
            db.query(ProtocolAlert).filter(ProtocolAlert.id == id,
                                           ProtocolAlert.protocol == protocol,
                                           ProtocolAlert.aidocId == aidocId).update(
                {ProtocolAlert.readFlag: False})
        db.commit()
    except:
        assert False
    # API call
    update_notifications = client.get("/api/pd_notification/update", params={
        "aidocId": aidocId, "id": id, "protocol": protocol, "action": action},
                                      headers=new_token_on_headers)

    assert update_notifications.status_code == status

    if update_notifications.status_code == 200:
        db_record = db.query(ProtocolAlert).filter(ProtocolAlert.id == id,
                                                   ProtocolAlert.protocol == protocol,
                                                   ProtocolAlert.aidocId == aidocId).one()
        if action == "delete":
            assert db_record.isActive is True
        elif action == "read":
            assert db_record.readFlag is False
