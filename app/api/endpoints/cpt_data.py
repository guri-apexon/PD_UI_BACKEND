from email import message
from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.utilities.extractor.prepare_cpt_section_data import PrepareUpdateData
from app.utilities.section_enriched import \
    update_section_data_with_enriched_data
from app.api import deps
from app.utilities.config import settings
from app.api.endpoints import auth
from app.utilities.redaction.protocol_view_redaction import \
    ProtocolViewRedaction
from fastapi.responses import JSONResponse
from fastapi import status
import logging
from fastapi import HTTPException, status


router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)


@router.get("/")
async def get_cpt_headers(
        aidoc_id: str = "",
        link_level: int = 1,
        toc: int = 0,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Get CPT Sections/Headers  list for a particular document.

    :param aidoc_id: document id
    :param link_level: level of headers in toc
    :param toc: is optional with value 0 or 1
    :param _: To validate API token
    :returns: list of all section/headers 
              if toc will be 1 link_level is 6 it will returs multi dimentional list according to parent child relationship
    """

    headers_dict = crud.get_document_links(aidoc_id, link_level, toc)
    return headers_dict


@router.get("/get_enriched_terms")
async def get_enriched_data(
        db: Session = Depends(deps.get_db),
        doc_id: str = "",
        link_id: str = "",
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Get clinical terms values for the enriched text as per doc and section id
    :param db: database session
    :param doc_id: document id
    :param link_id: link id of document as section id
    :param _: To validate API token
    :returns: To collect all the clinical terms values for the enriched text
    from all over the section
    """
    nlp_entity_data = crud.nlp_entity_content.get(db=db, doc_id=doc_id,
                                                  link_id=link_id)
    clinical_data = []
    for entity in nlp_entity_data:
        clinical_values = {
            'doc_id': entity.doc_id,
            'link_id': entity.link_id,
            'parent_id': entity.parent_id,
            'text': entity.standard_entity_name,
            'preferred_term': entity.iqv_standard_term,
            'ontology': entity.ontology,
            'synonyms': entity.entity_xref,
            'medical_term': "",
            'classification': entity.entity_class
        }
        clinical_data.append(clinical_values)
    return clinical_data


@router.get("/get_section_data")
async def get_cpt_section_data(
        psdb: Session = Depends(deps.get_db),
        aidoc_id: str = "",
        link_level: int = 1,
        link_id: str = "",
        userId: str = "",
        protocol: str = "",
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Get CPT Section/Header data for particular document
    :param psdb: database instance
    :param aidoc_id: document id
    :param link_level: level of headers in toc
    :param link_id: link id or section id
    :param protocol: protocol of document 
    :param userId: userid
    :param user: user optional
    :param _: To validate API token
    :returns: requested section/header data
              if document does not exist return json response with "docid does not exist"
    """
    iqv_document = crud.get_document_object(aidoc_id, link_level, link_id)
    if iqv_document is None:
        logger.info(f"Docid {aidoc_id} does not exists")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={
            "message": "This document is not available in our database"})
    protocol_view_redaction = ProtocolViewRedaction(userId, protocol)
    finalized_iqvxml = PrepareUpdateData(iqv_document,
                                         protocol_view_redaction.profile_details,
                                         protocol_view_redaction.entity_profile_genre)
    finalization_req_dict, _ = finalized_iqvxml.prepare_msg()

    # Collect the enriched data based on doc and link ids.
    enriched_data = await get_enriched_data(psdb, aidoc_id, link_id)
    section_with_enriched = update_section_data_with_enriched_data(
        section_data=finalization_req_dict, enriched_data=enriched_data)

    return section_with_enriched


@router.post("/update_enriched_data")
def create_enriched_data(
        *,
        db: Session = Depends(deps.get_db),
        doc_id: str = "",
        link_id: str = "",
        data: schemas.NlpEntityData,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Create new entity records with updated clinical terms
    :param db: database session
    :param doc_id: document id
    :param link_id: ink id of document as section id
    :param data: clinical terms
    :param _: To validate API token
    :returns: response with newly create record
    """
    enriched_data = crud.nlp_entity_content.save_data_to_db(db, doc_id, link_id,
                                                            data.data)
    return enriched_data


@router.get("/get_section_data_configurable_parameter")
async def get_cpt_section_data_with_configurable_parameter(
        psdb: Session = Depends(deps.get_db),
        aidoc_id: str = "",
        link_level: int = 1,
        link_id: str = "",
        section_text = "",
        user_id: str = "",
        protocol: str = "",
        config_variables: str = "",
        # _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Get CPT Section/Header data for particular document with Configurable
    terms values
    :param db: db session
    :param aidoc_id: document id
    :param link_level: level of headers in toc
    :param link_id: section id
    :param protocol: protocol of document
    :param user_id: userid
    :param clinical_terms: true/false -- optional
    :param time_points: true/false -- optional
    :param preferred_terms: true/false -- optional
    :param redaction_attributes: true/false -- optional
    :param references: true/false -- optional
    :param properties: true/false -- optional
    :param _ : API token validation
    :returns: Section data with configurable terms values
    """

    try:
        # Section data from the existing end point
        section_res = await get_cpt_section_data(psdb, aidoc_id, link_level, link_id,
                                                user_id, protocol)

        # Terms values based on given configuration values
        terms_values = crud.get_document_terms_data(psdb, aidoc_id,
                                                    link_id, config_variables,section_text)

        # enriched data from existing end point
        enriched_data = await get_enriched_data( psdb,aidoc_id,link_id)
        logger.info(f"config api result {section_res}, {terms_values}, {enriched_data}")

        return [section_res, terms_values, enriched_data]
    except Exception as e:
        logger.exception(f"exception occured in config api for doc_id {aidoc_id} and link_id {link_id} and exception is {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Exception to fetch configration data {str(e)}")
