import logging
from app.utilities.config import settings
from .model.iqvsectionlock_db import IqvsectionlockDb
from app.db.session import SessionLocal
import requests

logger = logging.getLogger(settings.LOGGER_NAME)


def get(data: dict):
    """
    get section lock info
    """
    with SessionLocal() as session:
        data = IqvsectionlockDb.get_record(session, data)
    return data


def put(data: dict):
    """
    put section lock info
    """
    with SessionLocal() as session:
        data = IqvsectionlockDb.update_record(session, data)
        session.commit()
    return data


def remove(data: dict):
    """
    remove section lock info
    """
    with SessionLocal() as session:
        session.query(IqvsectionlockDb).filter(
                IqvsectionlockDb.userId == data['userId']).delete()
        session.commit()

    # call management service for run work flow
    management_api_url = settings.MANAGEMENT_SERVICE_URL + "run_work_flow"
    _ = requests.post(management_api_url, data=data, headers=settings.MGMT_CRED_HEADERS)
    logger.info(f"workflow request sent to Management service")

    return data
