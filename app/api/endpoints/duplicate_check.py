from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.UserProtocolDocumentsDuplicateCheck)
def read_duplicate_attributes(
        db: Session = Depends(deps.get_db),
        sponser: str = "sponser",
        protocol: str = "protocol",
        VersionNumber: float = 0.0,
        Amendment: str = "Amendment",
) -> Any:
    """
    Retrieve Duplicate Attributes.
    """
    duplicate_attributes = crud.pd_user_protocol_document.duplicate_check(db, sponser, protocol, VersionNumber, Amendment, DocumentStatus="Final")
    return duplicate_attributes

