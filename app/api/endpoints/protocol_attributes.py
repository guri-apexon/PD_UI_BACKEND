from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.UserProtocolDocuments)
def read_protocol_attributes(
        db: Session = Depends(deps.get_db),
        id: str = "id",
) -> Any:
    """
    Retrieve Protocol Attributes.
    """
    protocol_attributes = crud.pd_user_protocol_document.get(db, id)
    return protocol_attributes


