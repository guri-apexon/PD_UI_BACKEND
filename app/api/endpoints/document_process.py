from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.DocumentProcess)
def get_status(
        db: Session = Depends(deps.get_db),
        id: str = "id",
) -> Any:
    """
    Get status.
    """
    doucment_process = crud.pd_document_process.get(db, id)
    return doucment_process

@router.post("/", response_model=schemas.DocumentProcess)
def create_status(
        *,
        db: Session = Depends(deps.get_db),
        document_process_in: schemas.DocumentProcessCreate,
) -> Any:
    """
    Create a post status.
    """
    document_process = crud.pd_document_process.create(db, obj_in=document_process_in)
    return document_process

