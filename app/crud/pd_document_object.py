from typing import Optional
import psycopg2
from etmfa_core.aidoc.io.load_xml_db_ext import GetIQVDocumentFromDB_with_doc_id
from app.db.session import psqlengine
from app.utilities.config import settings
import logging
from etmfa_core.aidoc.IQVDocumentFunctions import IQVDocument

logger = logging.getLogger(settings.LOGGER_NAME)


def get_document_object(aidoc_id: str, link_level: int, link_id: int) -> Optional[IQVDocument]:
    """
    :param aidoc_id: document id
    :param link_level: level of headers in toc
    :param link_id: link id of document 
    :returns: requested section/header data
    """

    try:
        connection = psqlengine.raw_connection()
        iqv_document = GetIQVDocumentFromDB_with_doc_id(
                connection, aidoc_id, link_level=link_level, link_id=link_id)
        return iqv_document
    except (Exception, psycopg2.Error) as error:
        logger.exception(f"Failed to get connection to postgresql : {error}, {aidoc_id}")
        return None
    finally:
        if connection:
            connection.close()