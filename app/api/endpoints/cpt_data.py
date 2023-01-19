from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud
from app.utilities.extractor.prepare_cpt_section_data import PrepareUpdateData
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


@router.get("/get_section_data")
async def get_cpt_section_data(
        db: Session = Depends(deps.get_db),
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
    return finalization_req_dict


@router.get("/get_section_data_configurable_parameter")
async def get_cpt_section_data_with_configurable_parameter(
        db: Session = Depends(deps.get_db),
        aidoc_id: str = "",
        link_level: int = 1,
        link_id: str = "",
        user_id: str = "",
        protocol: str = "",
        clinical_terms: bool = None,
        time_points: bool = None,
        preferred_terms: bool = None,
        redaction_attributes: bool = None,
        references: bool = None,
        properties: bool = None,
        _: str = Depends(auth.validate_user_token)
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
    section_with_terms = []

    # Section data from the existing end point
    section_res = await get_cpt_section_data(db, aidoc_id, link_level, link_id,
                                             user_id, protocol)
    section_with_terms.append(section_res)

    # Terms values based on given configuration values
    terms_values = crud.get_document_terms_data(db, aidoc_id, link_level,
                                                link_id, clinical_terms,
                                                time_points, preferred_terms,
                                                redaction_attributes,
                                                references, properties)
    section_with_terms.append(terms_values)

    return section_with_terms
