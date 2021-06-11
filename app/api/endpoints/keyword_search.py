import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from http import HTTPStatus

from app import crud, schemas
from app.api import deps
from app.utilities.config import settings
import json
router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)

@router.post("/")
def search_elastic(search_json_in: schemas.SearchJson, db: Session = Depends(deps.get_db)):
    try:
        logger.info("Received request in ES keyword_search.search_elastic: {}".format(search_json_in))
        res = crud.query_elastic(search_json_in, db)
    except Exception as ex:
        logger.exception("Exception Inside keyword_search.search_elastic:", ex)
        res = dict()
        res['ResponseCode'] = HTTPStatus.INTERNAL_SERVER_ERROR
        res['Message'] = str(ex)

    return (res)
