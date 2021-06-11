import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.utilities.config import settings

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)


@router.post("/")
def search_elastic(aidocid: str = "aidocid", db: Session = Depends(deps.get_db)):
    try:
        logger.info("Received qc elastic update request: " + str(aidocid))
        res = crud.qc_update_elastic(aidocid, db)
    except Exception as e:
        logger.error("Exception = ", e)
        res = dict()
        res['ResponseCode'] = 500
        res['Message'] = 'Internal Server Error'

    return (res)
