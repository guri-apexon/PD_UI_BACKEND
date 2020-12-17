from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.UserProtocolDocuments])
def read_related_protocols(
        db: Session = Depends(deps.get_db),
        Protocol: str = "protocol",
) -> Any:
    """
    Retrieve Protocol Attributes.
    """
    related_protocols = crud.pd_user_protocol_document.get_by_protocol(db, Protocol)
    return related_protocols
