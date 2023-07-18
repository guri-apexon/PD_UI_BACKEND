import logging
from app.utilities.config import settings
from .model.iqvsectionlock_db import IqvsectionlockDb
from app.db.session import SessionLocal
from .model.__base__ import get_utc_datetime
from sqlalchemy import extract
import requests
import json

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
    try:
        with SessionLocal() as session:
            data = IqvsectionlockDb.update_record(session, data)
            session.commit()
        return data
    except Exception as e:
        session.rollback()
        raise Exception(str(e))


def get_section_loc_records(doc_id: str):
    """
    To get section loc records based on document
    """
    try:
        with SessionLocal() as session:
            current_timestamp = get_utc_datetime()
            today_date = current_timestamp.date()
            # current day check is there section locks exits or not =>
            # sent validation error
            section_lock = session.query(IqvsectionlockDb).filter(
                IqvsectionlockDb.doc_id == doc_id, IqvsectionlockDb.link_id != '',
                extract('month', IqvsectionlockDb.last_updated) == today_date.month,
                extract('year', IqvsectionlockDb.last_updated) == today_date.year,
                extract('day', IqvsectionlockDb.last_updated) == today_date.day).all()
            if section_lock:
                return {'message': 'Another user is now using this document, Please try after some time'}
            else:
                # check is there dummy record available or not => no record =>
                # sent validation error
                section_lock = session.query(IqvsectionlockDb).filter(
                    IqvsectionlockDb.doc_id == doc_id,
                    IqvsectionlockDb.link_id == '',
                    IqvsectionlockDb.userId == '').first()
                if section_lock:
                    # Collect records of section lock and remove it
                    session.query(IqvsectionlockDb).filter(
                        IqvsectionlockDb.doc_id == doc_id).delete()
                else:
                    return {
                        'message': 'Document does not have any update to run workflow'}
            session.commit()
            return {'message': 'Success'}
    except Exception as e:
        session.rollback()
        raise Exception(str(e))


def remove(data: dict):
    """
    remove section lock info
    """
    doc_id = data.get('docId')
    section_loc = get_section_loc_records(doc_id=doc_id)

    if section_loc.get('message') != 'Success':
        return section_loc, False

    # call management service for run work flow
    del data['userId']
    management_api_url = settings.MANAGEMENT_SERVICE_URL + "run_work_flow"
    settings.MGMT_CRED_HEADERS.update({'Content-Type': 'application/json'})
    response = requests.post(management_api_url, data=json.dumps(data), headers=settings.MGMT_CRED_HEADERS)
    logger.info(f"workflow request sent to Management service")
    return {"message":response.json()}, True if response.status_code == 200 else False


def get_document_lock_status(data: dict):
    doc_id = data.get('doc_id')
    current_timestamp = get_utc_datetime()
    today_date = current_timestamp.date()
    with SessionLocal() as session:
        # current day check is there section locks exits or not
        section_lock = session.query(IqvsectionlockDb).filter(
            IqvsectionlockDb.doc_id == doc_id, IqvsectionlockDb.link_id != '',
            extract('month', IqvsectionlockDb.last_updated) == today_date.month,
            extract('year', IqvsectionlockDb.last_updated) == today_date.year,
            extract('day', IqvsectionlockDb.last_updated) == today_date.day).first()
        if section_lock:
            return True
        else:
            # check is there dummy record available or not
            section_lock = session.query(IqvsectionlockDb).filter(
                IqvsectionlockDb.doc_id == doc_id,
                IqvsectionlockDb.link_id == '', IqvsectionlockDb.userId == '').first()
            if section_lock:
                return True
    return False
