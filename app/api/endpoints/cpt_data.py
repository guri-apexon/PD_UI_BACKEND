from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from etmfa_core.aidoc.io.load_xml_db_ext import GetIQVDocumentFromDB_with_doc_id
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
import psycopg2

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)


@router.get("/")
async def get_cpt_headers(
        db: Session = Depends(deps.get_db),
        aidoc_id: str = "",
        link_level: int = 1,
        toc: int = 0,
        # _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Get CPT Sections/Headers  list for a particular document 
    Input
        aidoc_id and link_level is required and toc is optional with value 0 or 1
    Output
        returns list of all section/headers
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
    Input
        aidoc_id, link_level, protocol, userid are required and user is optional
    Output
        return requested section/header data
    """
    try:
        connection = psqlengine.raw_connection()
        iqv_document = GetIQVDocumentFromDB_with_doc_id(
                connection, aidoc_id, link_level=link_level, link_id=link_id)
        if iqv_document == None:
            logger.info(f"Docid {aidoc_id} does not exists")
            return JSONResponse(status_code=status.HTTP_206_PARTIAL_CONTENT,content={"message":"Docid does not exists"})
    except (Exception, psycopg2.Error) as error:
        logger.exception(f"Failed to get connection to postgresql : {error}")
    finally:
        if connection:
            connection.close()
    protocol_view_redaction = ProtocolViewRedaction(userId, protocol)
    finalization_req_dict = dict()
    finalized_iqvxml = PrepareUpdateData(iqv_document, protocol_view_redaction.profile_details,
                                         protocol_view_redaction.entity_profile_genre)
    finalization_req_dict, _ = finalized_iqvxml.prepare_msg()
    return finalization_req_dict
