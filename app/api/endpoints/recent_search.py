from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.SavedSearch])
def read_recent_search(
        db: Session = Depends(deps.get_db),
        user: str = "user",
) -> Any:
    """
    Retrieve recent searches.
    """
    recent_search = crud.pd_recent_search.get_by_user(db, user)
    return recent_search


@router.post("/", response_model=schemas.RecentSearch)
def create_recent_search(
        *,
        db: Session = Depends(deps.get_db),
        recent_search_in: schemas.RecentSearchCreate,
) -> Any:
    """
    Create a new recent search.
    """
    recent_search = crud.pd_recent_search.create(db, obj_in=recent_search_in)
    return recent_search
