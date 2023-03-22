import logging
from app.utilities.config import settings
from app.db.session import SessionLocal
from sqlalchemy import and_
from .model.__base__ import MissingParamException
from .model.iqvdocument_link_db import IqvdocumentlinkDb
from .model.iqvpage_roi_db import IqvpageroiDb

logger = logging.getLogger(settings.LOGGER_NAME)


def get_audit_info(session, data: dict):
    """
    get audit info
    """
    obj = None
    if data.get('type') in ['text', 'table', 'image']:
        obj = session.query(IqvpageroiDb).filter(
            IqvpageroiDb.id == data['line_id']).first()
        if not obj:
            _id = data['line_id']
            raise MissingParamException(f'{_id} in Iqvpageroi db ')

    elif data.get('type') == 'header':
        obj = session.query(IqvdocumentlinkDb).filter(and_(IqvdocumentlinkDb.doc_id == data.get('doc_id'), IqvdocumentlinkDb.link_id == data.get('link_id'),
                                                           IqvdocumentlinkDb.link_id_level2 == data.get(
            'link_id_level2'), IqvdocumentlinkDb.link_id_level3 == data.get('link_id_level3'),
            IqvdocumentlinkDb.link_id_level4 == data.get(
            'link_id_level4'), IqvdocumentlinkDb.link_id_level5 == data.get('link_id_level5'),
            IqvdocumentlinkDb.link_id_level6 == data.get(
            'link_id_level6'))).first()
        if not obj:
            raise MissingParamException(f' data in Iqvdocument link db ')
    if obj == None:
        raise MissingParamException(f' type ')
    data['audit_info'] = {"last_reviewed_date": obj.last_updated,
                          "last_reviewed_by": obj.userId, "total_no_review": obj.num_updates}
    return data


def get(data: dict):
    """
    get audit info
    """
    with SessionLocal() as session:
        data = get_audit_info(session, data)
    return data
