from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ProtocolMetadataDuplicateCheck)
def read_duplicate_attributes(
        db: Session = Depends(deps.get_db),
        sponsor: str = "sponsor",
        protocol: str = "protocol",
        versionNumber: str = "versionNumber",
        amendment: str = "amendment",
) -> Any:
    """
    Retrieve Duplicate Attributes.
    """
    duplicate_attributes = crud.pd_protocol_metadata.duplicate_check(db, sponsor, protocol, versionNumber, amendment, documentStatus="Final")
    return duplicate_attributes

