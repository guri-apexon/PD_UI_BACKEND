import pytest
import json
from app.db.session import SessionLocal
from app.main import app
from app.utilities.redact import redactor
from fastapi.testclient import TestClient

client = TestClient(app)
db = SessionLocal()
REDACT_STR = '~REDACTED~'


@pytest.mark.parametrize("aidoc_id, userId, protocol, user", [
    ("1fd2c7c3-394c-4ce3-9ed9-6ef0c92a836d", "1072234", "PD-SDS-PROT-S2", "normal"),
    ("1fd2c7c3-394c-4ce3-9ed9-6ef0c92a836d", "1072234", "TAK-861-1001", "normal"),
])
def test_redact_profile_view(new_token_on_headers, aidoc_id, userId, protocol, user):
    follow_response = client.get("/api/protocol_data/",
                                 params={"aidoc_id": aidoc_id, "userId": userId, "protocol": protocol,
                                         "user": user}, headers=new_token_on_headers)
    assert follow_response.status_code == 200
    content = json.loads(follow_response.content.decode('utf-8'))
    profile_name, _, _ = redactor.get_current_redact_profile(current_db=db, user_id=userId, protocol=protocol)
    if profile_name == 'profile_0':
        assert content['id'] is not None and content['documentFilePath'] is not None and content['iqvdataToc'] is not None
        assert REDACT_STR in content['iqvdataToc'] or REDACT_STR in content['iqvdataSoa'] \
               or REDACT_STR in content['iqvdataSummary']
    else:
        assert content['id'] is not None and content['documentFilePath'] is not None and content['iqvdataToc'] is not None
        assert REDACT_STR not in content['iqvdataToc'] and REDACT_STR not in content['iqvdataSoa'] \
               and REDACT_STR not in content['iqvdataSummary']
