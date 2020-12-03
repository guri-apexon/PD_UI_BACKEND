from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.UserProtocolDocuments])
def read_user_protocol_document(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve all Protocol Sponsors.
    """
    user_protocol_documents = crud.pd_user_protocol_document.get_multi(db, skip=skip, limit=limit)
    return user_protocol_documents


@router.post("/", response_model=schemas.UserProtocolDocuments)
def create_user_protocol_document(
        *,
        db: Session = Depends(deps.get_db),
        user_protocol_document_in: schemas.UserProtocolDocumentsCreate,
) -> Any:
    """
    Create a new protocol sponsor.
    """
    user_protocol_document = crud.pd_user_protocol_document.create(db, obj_in=user_protocol_document_in)
    return user_protocol_document
