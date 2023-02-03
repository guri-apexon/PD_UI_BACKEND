import logging
import os
from typing import Any
import pandas as pd

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from app import crud, schemas, config
from app.api import deps
from app.utilities.config import settings
from app import crud
from app.utilities.file_utils import validate_qc_protocol_file, save_request_file
from app.api.endpoints import auth
from app.utilities.redaction.protocol_view_redaction import ProtocolViewRedaction
from fastapi.responses import JSONResponse
router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)


@router.get("/", response_model=schemas.ProtocolData)
async def get_protocol_data(
        db: Session = Depends(deps.get_db),
        aidoc_id: str = "id",
        userId: str = "userId",
        protocol: str = "protocol",
        user: str = "user",
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Get protocol data.
    """

    try:
        protocol_view_redaction = ProtocolViewRedaction(userId, protocol)

        metadata_resource = crud.pd_protocol_metadata.get_by_id(db, id=aidoc_id)
        if protocol_view_redaction.profile_name == config.USERROLE_REDACTPROFILE_MAP["secondary"] \
                and metadata_resource.uploadDate <= pd.to_datetime(settings.LEGACY_PROTOCOL_UPLOAD_DATE):
            logger.exception(f'Secondary user trying to access document older than legacy_upload_date')
            raise HTTPException(status_code=401, detail=f"Secondary user trying to access document older than legacy_upload_date")

        protocol_data = protocol_view_redaction.redact_protocol_data(aidoc_id, user)
        headers = {"Cache-Control": "no-store"}
        return JSONResponse(content=protocol_data, headers=headers)
    except Exception as ex:
        logger.exception(f'pd-ui-backend: Exception occurred in rendering protocol-data {str(ex)}')
        raise HTTPException(status_code=401, detail=f"Exception occurred in rendering protocol-data {str(ex)}")


@router.get("/qc1_protocol_review_json")
def download_qc1_protocol_data_json(
        aidoc_id: str = None,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Retrieve all Protocol Sponsors.
    """
    try:
        iqvdata_json_file_path = crud.pd_protocol_data.generate_iqvdata_json_file(aidoc_id)
        return iqvdata_json_file_path
    except Exception as ex:
        logger.exception(f'pd-ui-backend: Exception occured in qc-protocol-data-json download {str(ex)}')
        raise HTTPException(status_code=401, detail=f"Exception in qc-protocol-data-json download {str(ex)}")


@router.get("/qc1_protocol_review_xlsx")
def download_qc1_protocol_data_xlsx(
        aidoc_id: str = None,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Retrieve all Protocol Sponsors.
    """
    try:
        iqvdata_xlsx_file_path = crud.pd_protocol_data.generate_iqvdata_xlsx_file(aidoc_id)
        return iqvdata_xlsx_file_path
    except Exception as ex:
        logger.exception(f'pd-ui-backend: Exception occured in qc-protocol-data-xlsx download {str(ex)}')
        raise HTTPException(status_code=401, detail=f"Exception in qc-protocol-data-xlsx download {str(ex)}")


@router.post("/qc1_protocol_upload")
async def qc1_protocol_upload(*,
                              iqvdata_xls_file: UploadFile = File(..., title="Updated IQVData JSON file",
                                                                  description="Upload Updated JSON file"),
                              aidoc_id: str,
                              db: Session = Depends(deps.get_db),
                              _: str = Depends(auth.validate_user_token)
                              ) -> Any:
    """
    Upload the qc1 protocol xml file
    """
    try:
        protocol_data_updation_status = ""
        protocol_file_path = save_request_file(aidoc_id, iqvdata_xls_file)['file_path']
        validate_qc_protocol_file(iqvdata_xls_file.content_type)

        uploaded_file_name_split = os.path.splitext(protocol_file_path)

        if uploaded_file_name_split[1] == ".json":
            protocol_data_updation_status = crud.pd_protocol_data.save_qc_jsondata_to_db(db, aidoc_id,
                                                                                         protocol_file_path)
        elif uploaded_file_name_split[1] == ".xlsx":
            protocol_data_updation_status = crud.pd_protocol_data.save_qc_exceldata_to_db(db, aidoc_id,
                                                                                          protocol_file_path)
        return protocol_data_updation_status
    except Exception as ex:
        logger.exception(f'pd-ui-backend: Exception occured in qc_protocol_upload {str(ex)}')
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail="Invalid Source/Target file received" + str(ex))
