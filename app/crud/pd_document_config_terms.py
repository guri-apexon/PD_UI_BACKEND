from app.utilities.config import settings
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(settings.LOGGER_NAME)


def get_document_terms_data(db: Session, aidoc_id: str, link_level: int,
                            link_id: str, clinical_terms: bool,
                            time_points: bool, preferred_terms: bool,
                            redaction_attributes: bool, references: bool,
                            properties: bool):
    """
    Collect terms values based on provided configuration values for the
    document section
    """
    terms_values = {}
    if clinical_terms:
        clinical_values = []
        terms_values.update({'clinical_terms': clinical_values})
    if time_points:
        time_points_values = []
        terms_values.update({'time_points': time_points_values})
    if preferred_terms:
        preferred_values = []
        terms_values.update({'preferred_terms': preferred_values})
    if redaction_attributes:
        redaction_att_values = []
        terms_values.update({'redaction_attributes': redaction_att_values})
    if references:
        references_values = []
        terms_values.update({'references': references_values})
    if properties:
        properties_values = []
        terms_values.update({'properties': properties_values})

    return [terms_values]
