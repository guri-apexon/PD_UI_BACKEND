from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Protocol])
def read_protocols(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve all Protocol Sponsors.
    """
    protocol = crud.pd_protocols.get_multi(db, skip=skip, limit=limit)
    return protocol


@router.post("/", response_model=schemas.Protocol)
def create_protocol_sponsor(
        *,
        db: Session = Depends(deps.get_db),
        protocol_in: schemas.ProtocolCreate,
) -> Any:
    """
    Create a new protocol sponsor.
    """
    protocol = crud.pd_protocols.create(db, obj_in=protocol_in)
    return protocol
