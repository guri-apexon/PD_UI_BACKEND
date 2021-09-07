from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.api.endpoints import auth

router = APIRouter()


@router.get("/", response_model=schemas.ProtocolMetadata)
def read_latest_approved_document_metadata(
        db: Session = Depends(deps.get_db),
        protocol: str = None,
        _: str = Depends(auth.validate_user_token),
) -> Any:
    """
    Retrieve all Protocol Sponsors.
    """
    protocol_metadata = crud.pd_protocol_metadata.get_latest_approved_document(db, protocol)
    return protocol_metadata