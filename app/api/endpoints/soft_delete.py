from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ProtocolDataReadIqvdata)
def get_protocol_data(
        db: Session = Depends(deps.get_db),
        id: str = "id",
) -> Any:
    """
    Get protocol data.
    """
    protocol_data = crud.pd_protocol_metadata.get_metadata_by_deleteCondition(db, id)
    return protocol_data

@router.post("/", response_model=schemas.MetadataSoftdelete)
def create_iqvdata(
        *,
        db: Session = Depends(deps.get_db),
        protocol_data_in: schemas.ProtocolDataCreate,
) -> Any:
    """
    Create a post status.
    """
    protocol_data = crud.pd_protocol_metadata.create(db, obj_in=protocol_data_in)
    return protocol_data
