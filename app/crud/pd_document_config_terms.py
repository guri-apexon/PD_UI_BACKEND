import imp
from app.utilities.config import settings
from sqlalchemy.orm import Session
import logging
from app.models.pd_iqvvisitrecord_db import IqvvisitrecordDb
from app.models.pd_nlp_entity_db import NlpentityDb
from app.models.pd_iqvdocumentlink_db import IqvdocumentlinkDb
from app.models.pd_iqvexternallink_db import IqvexternallinkDb
from app.models.pd_iqvkeyvalueset_db import IqvkeyvaluesetDb
from app.models.pd_documenttables_db import DocumenttablesDb
from app.utilities.extractor_config import ModuleConfig

logger = logging.getLogger(settings.LOGGER_NAME)


def get_document_terms_data(db: Session, aidoc_id: str, link_level: int,
                            link_id: str, config_variables: str, section_text: str) -> list:

    """
    Collect terms values based on provided configuration values for the
    document section
    terms values
    :param db: db session
    :param aidoc_id: document id
    :param link_level: level of headers in toc
    :param link_id: section id
    :param config_variables is string separated by ,
        :param clinical_terms -- optional
        :param time_points -- optional
        :param preferred_terms -- optional
        :param redaction_attributes -- optional
        :param references -- optional
        :param properties -- optional
    :returns: list of configurable terms values
    """

    if link_id:
        new_link_id = link_id
    elif section_text:
        try:        
            get_link_id = db.query(IqvdocumentlinkDb).filter(IqvdocumentlinkDb.doc_id == aidoc_id, IqvdocumentlinkDb.LinkText == section_text).one()
            new_link_id = get_link_id.link_id
        except Exception as e:
            new_link_id = ""    
    else:
        new_link_id = ""

    terms_values = {}

    if "time_points" in config_variables:        
        if new_link_id:
            iqv_time_point_visit_records = db.query(IqvvisitrecordDb).filter(IqvvisitrecordDb.doc_id == aidoc_id, IqvvisitrecordDb.table_roi_id == new_link_id).all()
        else:
            iqv_time_point_visit_records = db.query(IqvvisitrecordDb).filter(IqvvisitrecordDb.doc_id == aidoc_id).all()
        time_points_values = [{"id":iqvvisit_record.id,"time_point":iqvvisit_record.visit_timepoint,"table_roi_id":iqvvisit_record.table_roi_id} for iqvvisit_record in iqv_time_point_visit_records]
        terms_values.update({'time_points': time_points_values})
        logger.info(f"time points results {time_points_values}")
    
    if "clinical_terms" in config_variables:
        if new_link_id:
            clinical_terms = db.query(NlpentityDb).filter(NlpentityDb.doc_id == aidoc_id, NlpentityDb.link_id == new_link_id).all()
        else:
            clinical_terms = db.query(NlpentityDb).filter(NlpentityDb.doc_id == aidoc_id).all()

        clinical_values = [{"id":clinical_term.id,"ontology":clinical_term.ontology,"parent_id":clinical_term.parent_id,
                            "entity_key":clinical_term.entity_key, "text":clinical_term.text} for clinical_term in clinical_terms]
        terms_values.update({'clinical_terms': clinical_values})
        logger.info(f"clinical terms results {clinical_values}")

    if "preferred_terms" in config_variables:
        if new_link_id:
            all_term_data = db.query(IqvdocumentlinkDb).filter(IqvdocumentlinkDb.doc_id == aidoc_id, IqvdocumentlinkDb.link_id == new_link_id).all()
            all_term_data_from_tables = db.query(DocumenttablesDb).filter(DocumenttablesDb.doc_id == aidoc_id, DocumenttablesDb.link_id == new_link_id).all()
        else:
            all_term_data = db.query(IqvdocumentlinkDb).filter(IqvdocumentlinkDb.doc_id == aidoc_id).all()
            all_term_data_from_tables = db.query(DocumenttablesDb).filter(DocumenttablesDb.doc_id == aidoc_id).all()
    
        preferred_values = [{"id":term_record.id,"preferred_term":term_record.iqv_standard_term,"parent_id":term_record.parent_id} for term_record in all_term_data]
        preferred_values_from_tables = [{"id":tb_term_record.id,"preferred_term":tb_term_record.iqv_standard_term,"parent_id":tb_term_record.parent_id} for tb_term_record in all_term_data_from_tables]
        all_term_records = preferred_values+preferred_values_from_tables
        terms_values.update({'preferred_terms': all_term_records})
        logger.info(f"preferred terms results {all_term_records}")
        
    if "references" in config_variables:
        if new_link_id:
            reference_links = db.query(IqvexternallinkDb).filter(IqvexternallinkDb.doc_id == aidoc_id, IqvexternallinkDb.link_id == new_link_id).all()
        else:
            reference_links = db.query(IqvexternallinkDb).filter(IqvexternallinkDb.doc_id == aidoc_id).all()

        references_values = [{"id":reference_link.id,"source_text":reference_link.source_text,
                    "destination_link_id":reference_link.destination_link_id,
                    "destination_link_prefix":reference_link.destination_link_prefix,"parent_id":reference_link.parent_id,
                    "destination_link_text":reference_link.destination_link_text} for reference_link in reference_links]
        terms_values.update({'references': references_values})
        logger.info(f"references results {references_values}")
    
    if "properties" in config_variables:
        if new_link_id:
            property_data = db.query(IqvkeyvaluesetDb).filter(IqvkeyvaluesetDb.doc_id == aidoc_id, IqvkeyvaluesetDb.link_id == new_link_id).all()
        else:
            property_data = db.query(IqvkeyvaluesetDb).filter(IqvkeyvaluesetDb.doc_id == aidoc_id).all()

        properties_values = [{"id":property.id,"key":property.key,"value":property.value,"parent_id":property.parent_id} for property in property_data]
        terms_values.update({'properties': properties_values})
        logger.info(f"properties results {preferred_values}")

    if "redaction_attributes" in config_variables:
        if new_link_id:
            redaction_values = db.query(IqvkeyvaluesetDb).filter(IqvkeyvaluesetDb.doc_id == aidoc_id, IqvkeyvaluesetDb.key == ModuleConfig.GENERAL.REDACTION_SUBCATEGORY_KEY, IqvkeyvaluesetDb.link_id == new_link_id).all()
        else:
            redaction_values = db.query(IqvkeyvaluesetDb).filter(IqvkeyvaluesetDb.doc_id == aidoc_id, IqvkeyvaluesetDb.key == ModuleConfig.GENERAL.REDACTION_SUBCATEGORY_KEY).all()

        redaction_att_values = [{"id":redaction_record.id,"key":redaction_record.key,"value":redaction_record.value,"parent_id":redaction_record.parent_id} for redaction_record in redaction_values]
        terms_values.update({'redaction_attributes': redaction_att_values})
        logger.info(f"redaction attributes results {redaction_att_values}")

    return [terms_values]
