from app.qc_ingest.qc_ingest_text import process_text
from app.qc_ingest.qc_ingest_image import process_image
from app.qc_ingest.qc_ingest_table import process_table
import logging
from app.utilities.config import settings


logger = logging.getLogger(settings.LOGGER_NAME)


def process(payload: list):
    """ proceesing QC Ingest """
    try:
        info_dict = dict()
        if payload is not None and len(payload) > 0:
            for data in payload:
                if data.get('type') == "text" or data.get('type') == "header":
                    process_text(data, info_dict)
                if data.get('type') == "image":
                    process_image(data)
                if data.get('type') == "table":
                    process_table(data)
        return True
    except Exception as exc:
        logger.exception(
            f"Exception received in processing text data: {exc}")
        return False
