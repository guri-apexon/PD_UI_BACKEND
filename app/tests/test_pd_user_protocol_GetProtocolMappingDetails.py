from datetime import datetime
from typing import Optional
import pytest
from app import config
from app.crud.pd_user_protocols import pd_user_protocols
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient
from app.tests import utils as test_utils
from fastapi import status

client = TestClient(app)
db = SessionLocal()

@pytest.mark.parametrize("userId, protocol, expected_response",
                         [("q1020640","", status.HTTP_200_OK),
                          ("", "p434", status.HTTP_200_OK),
                          ("q1020640", "p434", status.HTTP_200_OK)
                          ])
def test_get_details_by_userid_protocol(new_token_on_headers, userId, protocol, expected_response):
        response = client.get("/api/user_protocol/read_user_protocols_by_userId_or_protocol",
                              params={"userId":userId, "protocol":protocol},
                              headers=new_token_on_headers)
        t = 1
        assert response.status_code == expected_response