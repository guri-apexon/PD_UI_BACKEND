from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.ProtocolMetadata])
def read_related_protocols(
        db: Session = Depends(deps.get_db),
        protocol: str = "protocol",
) -> Any:
    """
    Retrieve Protocol Attributes.
    """
    related_protocols = crud.pd_protocol_metadata.get_by_protocol(db, protocol)
    return related_protocols
