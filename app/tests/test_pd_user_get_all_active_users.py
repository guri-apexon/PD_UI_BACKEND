from fastapi import HTTPException
import pytest
from app.api.endpoints import pd_user_get_all_active_users
from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient
import json
from fastapi import status
from app.models.pd_user import User


client = TestClient(app)
db = SessionLocal()

def test_get_all_user():
    response = client.get("/api/user/read_all_users")
    assert response.status_code == 200