from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.api.endpoints import auth

router = APIRouter()


@router.get("/", response_model=schemas.ProtocolStatus)
def get_status(
        db: Session = Depends(deps.get_db),
        id: str = "id",
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Get status.
    """
    document_status = crud.pd_protocol_metadata.get(db, id)
    return document_status


