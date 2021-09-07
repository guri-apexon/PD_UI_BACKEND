from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.api.endpoints import auth

router = APIRouter()


@router.get("/", response_model=List[schemas.ProtocolMetadata])
def read_associated_docs(
        db: Session = Depends(deps.get_db),
        _: str = Depends(auth.validate_user_token),
        protocol: str = "protocol",
) -> Any:
    """
    Retrieve Protocol Attributes.
    """
    associated_docs = crud.pd_protocol_metadata.associated_docs_by_protocol(db, protocol)
    return associated_docs
