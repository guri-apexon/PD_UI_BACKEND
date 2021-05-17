import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.utilities.config import settings
import json
router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)

@router.post("/")
def search_elastic(search_json_in: schemas.SearchJson, db: Session = Depends(deps.get_db)):
    try:
        logger.info("Received request in ES keyword_search: {}".format(search_json_in))
        res = crud.query_elastic(search_json_in, db)
    except Exception as e:
        logger.exception("Exception = ", e)
        res = dict()
        res['ResponseCode'] = 500
        res['Message'] = 'Internal Server Error'

    return (res)
