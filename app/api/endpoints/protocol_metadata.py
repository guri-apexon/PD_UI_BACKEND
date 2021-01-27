from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.ProtocolMetadata])
def read_protocol_metadata(
        db: Session = Depends(deps.get_db),
        userId: str = None,
) -> Any:
    """
    Retrieve all Protocol Sponsors.
    """
    protocol_metadata = crud.pd_protocol_metadata.get_metadata_by_userId(db, userId)
    return protocol_metadata


@router.post("/", response_model=schemas.ProtocolMetadata)
def create_protocol_metadata(
        *,
        db: Session = Depends(deps.get_db),
        protocol_metadata_in: schemas.ProtocolMetadataCreate,
) -> Any:
    """
    Create a new protocol sponsor.
    """
    protocol_metadata = crud.pd_protocol_metadata.create(db, obj_in=protocol_metadata_in)
    return protocol_metadata
