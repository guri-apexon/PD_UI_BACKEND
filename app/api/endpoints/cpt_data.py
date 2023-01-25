from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud
from app.utilities.extractor.prepare_cpt_section_data import PrepareUpdateData
from app.utilities.section_enriched import \
    update_section_data_with_enriched_data
from app.api import deps
from app.utilities.config import settings
from app.api.endpoints import auth
from app.utilities.redaction.protocol_view_redaction import ProtocolViewRedaction
from app.db.session import psqlengine
from fastapi.responses import JSONResponse
from fastapi import status
import logging

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)


@router.get("/")
async def get_cpt_headers(
        db: Session = Depends(deps.get_db),
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
    :returns: list of all section/headers 
              if toc will be 1 link_level is 6 it will returs multi dimentional list according to parent child relationship
    """

    headers_dict = crud.get_document_links(aidoc_id, link_level, toc)
    return headers_dict


@router.get("/get_enriched_terms")
async def get_enriched_data(
        db: Session = Depends(deps.get_psqldb),
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
            'text': entity.standard_entity_name
        }
        clinical_terms = {'preferred_term': "", 'ontology': entity.ontology,
                          'synonyms': entity.entity_xref,
                          'medical_term': "", 'classification': ""}
        clinical_values.update(clinical_terms)
        clinical_data.append(clinical_values)
    return clinical_data


@router.get("/get_section_data")
async def get_cpt_section_data(
        db: Session = Depends(deps.get_db),
        psdb: Session = Depends(deps.get_psqldb),
        aidoc_id: str = "",
        link_level: int = 1,
        link_id: str = "",
        userId: str = "",
        protocol: str = "",
        user: str = "",
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Get CPT Section/Header data for particular document
    
    :param aidoc_id: document id
    :param link_level: level of headers in toc
    :param protocol: protocol of document 
    :param userid: userid 
    :param user: user optional
    :returns: requested section/header data
              if document does not exist return json response with "docid does not exist"
    """

    iqv_document = crud.get_document_object(aidoc_id,link_level,link_id)
    if iqv_document == None:
        logger.info(f"Docid {aidoc_id} does not exists")
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"message":"This document is not available in our database"})
    protocol_view_redaction = ProtocolViewRedaction(userId, protocol)
    finalization_req_dict = dict()
    finalized_iqvxml = PrepareUpdateData(iqv_document, protocol_view_redaction.profile_details,
                                         protocol_view_redaction.entity_profile_genre)
    finalization_req_dict, _ = finalized_iqvxml.prepare_msg()

    # Collect the enriched data based on doc and link ids.
    enriched_data = await get_enriched_data(psdb, aidoc_id, link_id)

    section_with_enriched = update_section_data_with_enriched_data(
        section_data=finalization_req_dict, enriched_data=enriched_data)

    return section_with_enriched
