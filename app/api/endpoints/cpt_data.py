from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.api import deps
from app.utilities.config import settings
from app.api.endpoints import auth
import logging


router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)


@router.post("/update_enriched_data")
def create_enriched_data(
        *,
        db: Session = Depends(deps.get_db),
        doc_id: str = "",
        link_id: str = "",
        operation_type: str = "",
        data: schemas.NlpEntityData,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Create new entity records with updated clinical terms
    :param db: database session
    :param doc_id: document id
    :param link_id: ink id of document as section id
    :param data: clinical terms
    :param _: To validate API token
    :returns: response with newly create record
    """
    enriched_data = crud.nlp_entity_content.save_data_to_db(db, doc_id, link_id,operation_type,
                                                            data.data)
    return enriched_data

