import logging
from app.utilities.config import settings
from .model.iqvsectionlock_db import IqvsectionlockDb
from app.db.session import SessionLocal

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


def get_document_lock_status(data: dict):
    with SessionLocal() as session:
        data = IqvsectionlockDb.get_doc_lock_status(session, data)
    return data
