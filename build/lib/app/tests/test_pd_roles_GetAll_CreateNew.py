from app.db.session import SessionLocal
from app.main import app
from fastapi.testclient import TestClient
import pytest
from fastapi import status
from app.crud.pd_roles import roles
from app.models.pd_roles import Roles

client = TestClient(app)
db = SessionLocal()

def test_get_all_roles(new_token_on_headers):
    response = client.get("/api/roles/get_all_roles", headers=new_token_on_headers)
    if response.status_code == 200:
        assert len(response.json())>0

@pytest.mark.parametrize("insert_flag, roleName, roleDescription, roleLevel, expected_response",
                         [("0","normalrole","normaldescription", "secondary", status.HTTP_422_UNPROCESSABLE_ENTITY),
                          ("0", "", "description", "secondary",status.HTTP_422_UNPROCESSABLE_ENTITY),
                          ("0", "", "", "primary", status.HTTP_422_UNPROCESSABLE_ENTITY),
                          ("0", "", "", "", status.HTTP_422_UNPROCESSABLE_ENTITY),
                          ("1", "newuser", "userfortestingpostmethod", "secondary", status.HTTP_200_OK)])
def test_create_new_role(insert_flag, roleName, roleDescription, roleLevel, expected_response, new_token_on_headers):
    if insert_flag == "1":
        role_delete = db.query(Roles).filter(Roles.roleName == "newuser").delete()
        return role_delete
    create_new_role = client.post("/api/roles/new_role", json={"roleName":roleName, "roleDescription":roleDescription,
                                                               "roleLevel":roleLevel},
                                  headers=new_token_on_headers)
    assert create_new_role.status_code == expected_response