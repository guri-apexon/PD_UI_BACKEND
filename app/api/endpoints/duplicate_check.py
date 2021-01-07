from typing import Any, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ProtocolMetadataDuplicateCheck)
def read_duplicate_attributes(
        db: Session = Depends(deps.get_db),
        sponsor: str = "sponsor",
        protocolNumber: str = "protocolNumber",
        versionNumber: str = "versionNumber",
        amendmentNumber: str = "amendmentNumber",
) -> Any:
    """
    Retrieve Duplicate Attributes.
    """
    duplicate_attributes = crud.pd_protocol_metadata.duplicate_check(db, sponsor, protocolNumber, versionNumber, amendmentNumber, documentStatus="final")
    return duplicate_attributes
