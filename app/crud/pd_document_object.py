from typing import Optional
import psycopg2
from etmfa_core.aidoc.io.load_xml_db_ext import GetIQVDocumentFromDB_with_doc_id,GetIQVDocumentFromDB_with_imagebinaries
from app.db.session import psqlengine
from app.utilities.config import settings
import logging
from etmfa_core.aidoc.IQVDocumentFunctions import IQVDocument

logger = logging.getLogger(settings.LOGGER_NAME)


def get_document_object(aidoc_id: str, link_level: int = -1, link_id: str = None) -> Optional[IQVDocument]:
    """
    :param aidoc_id: document id
    :param link_level: level of headers in toc
    :param link_id: link id of particular section 
    :returns: requested section/header data
    """

    try:
        connection = None
        connection = psqlengine.raw_connection()
        headers_only = False
        include_images = True

        iqv_document,imagebinaries = GetIQVDocumentFromDB_with_imagebinaries(connection,
                                                                             aidoc_id,
                                                                             headers_only,
                                                                             link_level,
                                                                             link_id,
                                                                             include_images=include_images)

    except (Exception, psycopg2.Error) as error:
        logger.exception(f"Failed to get connection to postgresql : {error}, {aidoc_id}")
        iqv_document, imagebinaries = None, None
    finally:
        if connection:
            connection.close()

    return iqv_document, imagebinaries