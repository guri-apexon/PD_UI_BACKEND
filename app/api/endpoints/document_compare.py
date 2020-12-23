from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.DocumentCompare)
def get_compare_doc(
        db: Session = Depends(deps.get_db),
        id1: str = "id",
        id2: str = "id2"
) -> Any:
    """
    Get status.
    """
    doucment_process = crud.pd_document_compare.get_by_docId(db, id1, id2)
    return doucment_process

@router.post("/", response_model=schemas.DocumentCompare)
def create_compare_doc(
        *,
        db: Session = Depends(deps.get_db),
        document_compare_in: schemas.DocumentCompareCreate,
) -> Any:
    """
    Create a post status.
    """
    document_compare = crud.pd_document_compare.create(db, obj_in=document_compare_in)
    return document_compare

