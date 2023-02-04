from typing import Any, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.api.endpoints import auth

router = APIRouter()


@router.get("/", response_model=schemas.ProtocolMetadataDuplicateCheck)
def read_duplicate_attributes(
        db: Session = Depends(deps.get_db),
        sponsor: str = None,
        protocolNumber: str = None,
        versionNumber: str = None,
        amendmentNumber: str = None,
        documentStatus: str = None,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Retrieve Duplicate Attributes.
    """
    duplicate_attributes = crud.pd_protocol_metadata.duplicate_check(db, sponsor, protocolNumber, versionNumber, amendmentNumber, documentStatus)
    return duplicate_attributes
