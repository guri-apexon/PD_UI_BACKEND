import pytest
from app import crud, schemas
from app.main import app
from fastapi.testclient import TestClient
from app.db.session import SessionLocal

from app.models.pd_protocol_alert import ProtocolAlert
from sqlalchemy import and_
from app.crud.pd_user_alert import pd_user_alert
from http import HTTPStatus

client = TestClient(app)


@pytest.mark.parametrize(
    ["id", "protocol", "aidocId", "readFlag", "notification_delete" ,"insert_flag", "comment"],
    [
        ("611", "test_compare_0213_K-877-302", "8410e658-074a-4c6e-a45d-010d1663a0ca", True, False, 1, "To be inserted into db as correct id, aidocid and protocol number combination."),
        ("611", "test_compare_0213_K-877-302", "8410e658-074a-4c6e-a45d-010d1663a0ca", True, True, 1, "To be inserted into db as correct id, aidocid and protocol number combination and verifies notification_delete."),
        ("610", "test_compare_0213_K-877-302", "8410e658-074a-4c6e-a45d-010d1663a0ca", True, False, 0, "Not to be inserted into db as incorrect id (incorrect id), aidocid and protocol number combination."),
        ("611", "test_compare_0213_K-877-30", "8410e658-074a-4c6e-a45d-010d1663a0ca", True, False, 0, "Not to be inserted into db as incorrect id, aidocid (incorrect aidocid) and protocol number combination."),
        ("611", "test_compare_0213_K-877-302", "8410e658-074a-4c6e-a45d-010d1663a0c", True, False, 0, "Not to be inserted into db as incorrect id, aidocid and protocol number (incorrect aidocid) combination.")

     ])
def test_notification_read(id, protocol, aidocId, readFlag, notification_delete, insert_flag, comment):

    notification_read_in = schemas.NotificationRead()
    notification_read_in.id = id
    notification_read_in.protocol = protocol
    notification_read_in.aidocId = aidocId
    notification_read_in.readFlag = readFlag
    notification_read_in.notification_delete = notification_delete


    try:
        db = SessionLocal()

        protocol_alert = db.query(ProtocolAlert).filter(and_(ProtocolAlert.aidocId == notification_read_in.aidocId,
                                                             ProtocolAlert.id == notification_read_in.id,
                                                             ProtocolAlert.protocol == notification_read_in.protocol)).first()

        if protocol_alert:
            protocol_alert.readFlag = False
            protocol_alert.readTime = None
            protocol_alert.notification_delete = False
            db.add(protocol_alert)
            db.commit()

        response = pd_user_alert.update_notification_read_status(notification_read_in, db)

        if insert_flag:
            assert response['ResponseCode'] == HTTPStatus.OK
        elif insert_flag == False:
            assert response['ResponseCode'] in [HTTPStatus.NOT_ACCEPTABLE, HTTPStatus.NO_CONTENT]

    except Exception as ex:
        assert False


