from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.SavedSearch])
def read_saved_search(
        db: Session = Depends(deps.get_db),
        userId: str = "userId",
) -> Any:
    """
    Retrieve saved searches.
    """
    saved_search = crud.pd_saved_search.get_by_userId(db, userId)
    return saved_search


@router.post("/", response_model=schemas.SavedSearch)
def create_saved_search(
        *,
        db: Session = Depends(deps.get_db),
        saved_search_in: schemas.SavedSearchCreate,
) -> Any:
    """
    Create a new saved search.
    """
    saved_search = crud.pd_saved_search.create(db, obj_in=saved_search_in)
    return saved_search

@router.delete("/", response_model=schemas.SavedSearch)
def delete_saved_search(
        *,
        db: Session = Depends(deps.get_db),
        id: int = 0,
) -> Any:
    """
    Delete a saved search.
    """
    saved_search = crud.pd_saved_search.remove(db, id=id)
    return saved_search

