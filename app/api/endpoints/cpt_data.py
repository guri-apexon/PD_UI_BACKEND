import logging
import os
from typing import Any
import pandas as pd

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import schemas, config
from app.api import deps
from app.utilities.config import settings
from app import crud
from app.utilities.file_utils import validate_qc_protocol_file, save_request_file
from app.api.endpoints import auth
from app.utilities.redaction.protocol_view_redaction import ProtocolViewRedaction
from fastapi.responses import JSONResponse
router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)



@router.get("/")
async def get_cpt_headers(
        db: Session = Depends(deps.get_db),
        aidoc_id: str = "id",
        link_level: int = 1,
        toc: int=0,
        _: str = Depends(auth.validate_user_token)
) -> Any:

    headers_dict = crud.get_document_links(aidoc_id, link_level, toc)

    return headers_dict

@router.get("/get_section_data")
async def get_cpt_section_data(
        db: Session = Depends(deps.get_db),
        aidoc_id: str = "id",
        link_level: int = 1,
        link_id:str = '',
        userId: str = "userId",
        protocol: str = "protocol",
        user: str = "user",
        _: str = Depends(auth.validate_user_token)
) -> Any:
    import time
    import json

    from etmfa_core.aidoc.io.load_xml_db_ext import GetIQVDocumentFromDB_with_doc_id, GetIQVDocumentFromDB_headers
    import psycopg2
    st = time.time()
    conn = psycopg2.connect(database="pd_dev", user='app_pd_dev_dbo', password='pdi8ujnydev45678dbo',
                            host='10.3.67.93', port='5432')  # postgre dev server
    iqv_document = GetIQVDocumentFromDB_with_doc_id(conn, aidoc_id, link_level = link_level, link_id = link_id)
    ed = time.time()
    diff = ed - st
    print(f'diff = {diff}')

    from app.api.endpoints.etmfa_finalization.messaging.prepare_update_data import PrepareUpdateData
    print("prepareupdatedata")

    protocol_view_redaction = ProtocolViewRedaction(userId, protocol)
    print("protocol_view_redaction", protocol_view_redaction)
    st = time.time()
    finalization_req_dict = dict()
    print("finalization_req_dict", finalization_req_dict)
    finalized_iqvxml = PrepareUpdateData(iqv_document, 0, protocol_view_redaction.profile_details,
                                         protocol_view_redaction.entity_profile_genre)
    print("finalized_iqvxml", finalized_iqvxml)
    # finalization_req_dict["db_data"], updated_iqv_document = finalized_iqvxml.prepare_msg()
    finalization_req_dict, updated_iqv_document = finalized_iqvxml.prepare_msg()


    ed = time.time()
    diff = ed - st
    print(f'Finalization completion time = {diff}')

    return finalization_req_dict