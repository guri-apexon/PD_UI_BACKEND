from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from etmfa_core.aidoc.io.load_xml_db_ext import GetIQVDocumentFromDB_with_doc_id
from app import crud
from app.utilities.iqvdata_extractor.prepare_update_data import PrepareUpdateData
from app.api import deps
from app.utilities.config import settings
from app.api.endpoints import auth
from app.utilities.redaction.protocol_view_redaction import ProtocolViewRedaction
from app.db.session import psqlengine
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
        _: str = Depends(auth.validate_user_token)
) -> Any:

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
    try:
        connection = psqlengine.raw_connection()
        iqv_document = GetIQVDocumentFromDB_with_doc_id(
                connection, aidoc_id, link_level=link_level, link_id=link_id)
    except (Exception, psycopg2.Error) as error:
        print("Failed to get connection to PostgreSQL, error:", error)
    finally:
        if connection:
            connection.close()
    protocol_view_redaction = ProtocolViewRedaction(userId, protocol)
    finalization_req_dict = dict()
    finalized_iqvxml = PrepareUpdateData(iqv_document, 0, protocol_view_redaction.profile_details,
                                         protocol_view_redaction.entity_profile_genre)
    finalization_req_dict, updated_iqv_document = finalized_iqvxml.prepare_msg()
    return finalization_req_dict
