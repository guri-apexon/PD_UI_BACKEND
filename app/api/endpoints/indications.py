from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Indications])
def read_indications(
        db: Session = Depends(deps.get_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    indications = crud.pd_indication.get_multi(db, skip=skip, limit=limit)
    return indications


@router.post("/", response_model=schemas.Indications)
def create_indication(
        *,
        db: Session = Depends(deps.get_db),
        indication_in: schemas.IndicationsCreate,
) -> Any:
    """
    Create a new indication.
    """
    indication = crud.pd_indication.create(db, obj_in=indication_in)
    return indication
