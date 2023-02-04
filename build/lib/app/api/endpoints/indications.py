from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.api.endpoints import auth

router = APIRouter()


@router.get("/", response_model=List[schemas.Indications])
def read_indications(
        db: Session = Depends(deps.get_db),
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Retrieve users.
    """
    indications = crud.pd_indication.get_all_indications_sorted(db)
    return indications


@router.post("/", response_model=schemas.Indications)
def create_indication(
        *,
        db: Session = Depends(deps.get_db),
        indication_in: schemas.IndicationsCreate,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Create a new indication.
    """
    indication = crud.pd_indication.create(db, obj_in=indication_in)
    return indication
