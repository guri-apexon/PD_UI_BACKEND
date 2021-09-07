from datetime import datetime

import pytest
from app import config
from app.crud.pd_user_protocols import pd_user_protocols
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient
from app.tests import utils as test_utils

client = TestClient(app)
db = SessionLocal()


@pytest.mark.parametrize("insert_flg, user_id, protocol, follow_flg, user_role, expected_user_role", [
("0", "1034911", "SSR_1002-043", True, "secondary", "secondary"),
("0", "1034911", "SSR_1002-043", False, "secondary", "secondary"),
("0", "1034911", "SSR_1002-043", False, "", config.FOLLOW_DEFAULT_ROLE),
("0", "1034911", "SSR_1002-043", False, "xyz", config.FOLLOW_DEFAULT_ROLE),
("1", "1034911", "SSR_1002-043", True, "secondary", "secondary"),
("1", "1034911", "SSR_1002-043", False, "secondary", "secondary"),
("1", "1034911", "SSR_1002-043", False, "", config.FOLLOW_DEFAULT_ROLE),
("1", "1034911", "SSR_1002-043", False, "xyz", config.FOLLOW_DEFAULT_ROLE),
("0", "1034911", "SSR_1002-043", False, "primary", "primary"),
("1", "1034911", "SSR_1002-043", True, "primary", "primary")
])
def test_follow_protocol(new_token_on_headers, insert_flg, user_id, protocol, follow_flg, user_role, expected_user_role):
    current_timestamp = datetime.utcnow()

    if insert_flg:
        follow_record = pd_user_protocols.get_by_userid_protocol(db = db, userid = user_id, protocol = protocol)
        if follow_record:
            _ = pd_user_protocols.remove_followed_protocols(db, id = follow_record.id, userId = user_id)

    follow_response = client.post("/api/follow_protocol/", json={"userId": user_id,  "protocol": protocol,  "follow": follow_flg,  "userRole": user_role}, 
                                        headers = new_token_on_headers)
    assert follow_response.status_code == 200

    follow_record = pd_user_protocols.get_by_userid_protocol(db = db, userid = user_id, protocol = protocol)
    assert follow_record.follow == follow_flg
    assert follow_record.userRole == expected_user_role
    assert follow_record.isActive == True
    assert follow_record.lastUpdated >= current_timestamp

    if insert_flg:
        assert follow_record.timeCreated == follow_record.lastUpdated
