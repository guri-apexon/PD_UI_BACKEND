from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.MetadataSoftdelete])
def get_metadata_on_delete_condition(
        db: Session = Depends(deps.get_db),
        userId: str = None,
        protocol: str = None,
) -> Any:
    """
    Get protocol data.
    """
    records = crud.pd_protocol_metadata.get_records_by_filter_condition(db, userId, protocol)

    deleted_data = crud.pd_protocol_metadata.get_metadata_by_deleteCondition(db, records)
    return deleted_data

@router.post("/", response_model=schemas.MetadataSoftdelete)
def create_soft_delete(
        *,
        db: Session = Depends(deps.get_db),
        protocol_metadata_soft_delete_in: schemas.ProtocolMetadataSoftDeleteCreate,
) -> Any:
    """
    Create a post status.
    """
    protocol_metadata = crud.pd_protocol_metadata.create_soft_delete(db, obj_in=protocol_metadata_soft_delete_in)
    return protocol_metadata
