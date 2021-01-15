from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.ProtocolMetadata])
def read_lastest_apporved_document_metadata(
        db: Session = Depends(deps.get_db),
        protocol: str = None,
) -> Any:
    """
    Retrieve all Protocol Sponsors.
    """
    protocol_metadata = crud.pd_protocol_metadata.get_latest_approved_document(db, protocol)
    return protocol_metadata