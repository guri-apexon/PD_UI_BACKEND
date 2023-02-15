from datetime import datetime

import pytest
from app import config
from app.crud.pd_user_protocols import pd_user_protocols
from app.models.pd_user_protocols import PD_User_Protocols
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
db = SessionLocal()

@pytest.mark.parametrize("user_id, protocol, primary_flg", [
    ("1034911", "AKB-6548-CI-0014_SSR_1027", 1),
    ("1061485", "AKB-6548-CI-0014_SSR_1027", 0)
])
def test_is_user_primary_api(new_token_on_headers, user_id, protocol, primary_flg):

    is_primary = client.get("/api/user_protocol/is_primary_user", params={"userId": user_id, "protocol":protocol}, headers=new_token_on_headers)
    is_primary = is_primary.json()

    assert is_primary == primary_flg

@pytest.mark.parametrize("insert_flg, user_id, protocol, follow_flg, user_role, expected_user_role, expected_redact_profile", [
    ("0", "1034911", "SSR_1002-043", True, "secondary", "secondary", config.USERROLE_REDACTPROFILE_MAP.get("secondary", "")),
    ("0", "1034911", "SSR_1002-043", False, "secondary", "secondary", config.USERROLE_REDACTPROFILE_MAP.get("secondary", "")),
    ("0", "1034911", "SSR_1002-043", False, "", config.FOLLOW_DEFAULT_ROLE, config.USERROLE_REDACTPROFILE_MAP.get(config.FOLLOW_DEFAULT_ROLE, "")),
    ("0", "1034911", "SSR_1002-043", False, "xyz", config.FOLLOW_DEFAULT_ROLE, config.USERROLE_REDACTPROFILE_MAP.get(config.FOLLOW_DEFAULT_ROLE, "")),
    ("1", "1034911", "SSR_1002-043", True, "secondary", "secondary", config.USERROLE_REDACTPROFILE_MAP.get("secondary", "")),
    ("1", "1034911", "SSR_1002-043", False, "secondary", "secondary", config.USERROLE_REDACTPROFILE_MAP.get("secondary", "")),
    ("1", "1034911", "SSR_1002-043", False, "", config.FOLLOW_DEFAULT_ROLE, config.USERROLE_REDACTPROFILE_MAP.get(config.FOLLOW_DEFAULT_ROLE, "")),
    ("1", "1034911", "SSR_1002-043", False, "xyz", config.FOLLOW_DEFAULT_ROLE, config.USERROLE_REDACTPROFILE_MAP.get(config.FOLLOW_DEFAULT_ROLE, "")),
    ("0", "1034911", "SSR_1002-043", False, "primary", "primary", config.USERROLE_REDACTPROFILE_MAP.get("primary", "")),
    ("1", "1034911", "SSR_1002-043", True, "primary", "primary", config.USERROLE_REDACTPROFILE_MAP.get("primary", ""))
])
def test_follow_protocol(new_token_on_headers, insert_flg, user_id, protocol, follow_flg,
                         user_role, expected_user_role, expected_redact_profile):
    current_timestamp = datetime.utcnow()

    if insert_flg:
        follow_record = pd_user_protocols.get_by_userid_protocol(db=db, userid=user_id, protocol=protocol)
        if follow_record:
            _ = pd_user_protocols.remove_followed_protocols(db, id=follow_record.id, userId=user_id)

    follow_response = client.post("/api/follow_protocol/", json={"userId": user_id,  "protocol": protocol,
                                                                 "follow": follow_flg,  "userRole": user_role},
                                  headers=new_token_on_headers)
    assert follow_response.status_code == 200

    follow_record = pd_user_protocols.get_by_userid_protocol(db=db, userid=user_id, protocol=protocol)
    assert follow_record.follow == follow_flg
    assert follow_record.userRole == expected_user_role
    assert follow_record.isActive is True
    assert follow_record.redactProfile == expected_redact_profile
    assert str(follow_record.lastUpdated) >= str(current_timestamp)

    if insert_flg:
        assert follow_record.timeCreated == follow_record.lastUpdated


@pytest.mark.parametrize("user_id, protocol, follow_flg, user_role, project_id, expected_json, status_code", [
    ("1012424", "SSR_1002-043", True, "primary", "pid", {'userId': '1012424', 'protocol': 'SSR_1002-043', 'userRole': 'primary', 'userCreated': None, 'userUpdated': None}, 200),
    ("1012424", "SSR_1002-043", True, "primary", "pid", {'detail': "Mapping for userId: 1012424, protocol: SSR_1002-043 is already available & mapped"}, 403),
    ("", "SSR_1002-043", True, "primary", "pid", {'detail': "Can't Add with null values userId:, protocol:SSR_1002-043, follow:True & userRole:primary"}, 403)
])
def test_user_protocol_exists(new_token_on_headers, user_id, protocol, follow_flg, user_role, project_id, expected_json, status_code):
    sample_query_json = {
        "userId": user_id,
        "protocol": protocol,
        "userRole": user_role,
        "follow": follow_flg,
        "projectId": project_id
    }

    if status_code == 200:
        user_protocol = pd_user_protocols.userId_protocol_check(db, user_id, protocol)
        if user_protocol:
            db.delete(user_protocol)
            db.commit()

    response = client.post("/api/user_protocol/", json=sample_query_json, headers=new_token_on_headers)
    assert response.status_code == status_code
    response_json = response.json()
    if status_code == 200:
        response_json.pop('id')

    assert response_json == expected_json

@pytest.mark.parametrize("user_id, protocol, status_code", [
    ("1034911", "AKB-6548-CI-0014_SSR_1027", 200),
    ("1061485", "AKB-6548-CI-0014_SSR_1027", 404)
])
def test_user_protocol_delete(new_token_on_headers, user_id, protocol, status_code):

    response = client.delete("/api/user_protocol/", params={"userId": user_id, "protocol":protocol}, headers=new_token_on_headers)

    if response.status_code == 200:
        user_protocol = pd_user_protocols.userId_protocol_check(db, user_id, protocol)
        if user_protocol:
            user_protocol.isActive = True
            db.commit()
            db.refresh(user_protocol)

    assert response.status_code == status_code