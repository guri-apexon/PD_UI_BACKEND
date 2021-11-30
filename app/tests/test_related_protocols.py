import pytest
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
db = SessionLocal()

@pytest.mark.parametrize("user_id, protocol, user_role", [
    ("1034911", "AKB-6548-CI-0014_SSR_1027", 'primary'),
    ("1061485", "AKB-6548-CI-0014_SSR_1027", 'secondary')
])
def test_related_protocol(new_token_on_headers, user_id, protocol, user_role):

    response = client.get("/api/Related_protocols", params={"userId": user_id, "protocol":protocol}, headers=new_token_on_headers)
    response = response.json()

    for res in response:
        assert res.get('userRole', '') == user_role