from typing import Any
from fastapi import APIRouter, Depends
from app import crud, schemas
from app.api.endpoints import auth

router = APIRouter()


@router.post("/", response_model=schemas.LdapUserDetails)
def get_ldap_user_details(
        userId: str,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Retrieve Ldap User Details.
    """
    user_details = crud.get_ldap_user_details(userId)
    return user_details

