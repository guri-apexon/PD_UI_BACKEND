import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.utilities.config import settings

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)

logger.info("Keyword search import successful")


@router.post("/")
def search_elastic(search_json_in: schemas.SearchJson, db: Session = Depends(deps.get_db)):
    try:
        logger.info("Received request: ", search_json_in)

        res = crud.query_elastic(search_json_in, db)
    except Exception as e:
        logger.info("Exception = ", e)
        res = False

    return (res)
