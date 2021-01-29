from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.ProtocolSponsor])
def read_protocol_sponsors(
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve all Protocol Sponsors.
    """
    protocol_sponsors = crud.pd_protocol_sponsor.get_all(db)
    return protocol_sponsors


@router.post("/", response_model=schemas.ProtocolSponsor)
def create_protocol_sponsor(
        *,
        db: Session = Depends(deps.get_db),
        protocol_sponsor_in: schemas.ProtocolSponsorCreate,
) -> Any:
    """
    Create a new protocol sponsor.
    """
    protocol_sponsor = crud.pd_protocol_sponsor.create(db, obj_in=protocol_sponsor_in)
    return protocol_sponsor
