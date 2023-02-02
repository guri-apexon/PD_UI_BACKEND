from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.api.endpoints import auth

router = APIRouter()



@router.post("/", response_model=schemas.NlpEntityBase)
def create_enriched_data(
        *,
        db: Session = Depends(deps.get_db),
        nlp_entity_in: schemas.NlpEntityCreate,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Create a new enriched data.
    """
    enriched_data = crud.pd_nlp_entity.create(db, obj_in=nlp_entity_in)
    return enriched_data
