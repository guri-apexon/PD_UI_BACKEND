import logging
from app.utilities.config import settings

from app.models.pd_nlp_entity_db import NlpentityDb
from sqlalchemy.orm import Session

logger = logging.getLogger(settings.LOGGER_NAME)


class NlpEntityCrud(NlpentityDb):
    """
    NLP Entity crud operation to get entity object with clinical terms.
    """

    def get(self, db: Session, doc_id: str, link_id: str):
        try:
            all_term_data = db.query(NlpentityDb).filter(
                NlpentityDb.doc_id == doc_id).filter(
                NlpentityDb.link_id == link_id).all()
        except Exception as ex:
            all_term_data = []
            logger.exception("Exception in retrieval of data from table", ex)
        return all_term_data


nlp_entity_content = NlpEntityCrud()
