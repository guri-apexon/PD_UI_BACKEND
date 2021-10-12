import logging
import os
from typing import Any

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from app import crud, schemas, config
from app.api import deps
from app.utilities.config import settings
from app import crud
from app.utilities.file_utils import save_json_file, validate_qc_protocol_file, save_request_file
from app.api.endpoints import auth
from pathlib import Path

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)


@router.get("/", response_model=schemas.ProtocolQcData)
def get_protocol_qcdata(
        db: Session = Depends(deps.get_db),
        id: str = "id",
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Get protocol QC data.
    """
    protocol_qcdata, json_filename = crud.pd_protocol_qcdata.save_db_jsondata_to_file(db = db, aidoc_id = id, file_prefix=config.QC_WIP_SRC_DB_FILE_PREFIX)
    logger.info(f"Generated {json_filename}")
    return protocol_qcdata


@router.post("/qc1_protocol_upload")
async def qc1_protocol_upload(*,
                              uploaded_json_file: UploadFile = File(..., title="Updated IQVData JSON file",
                                                                  description="Upload Updated JSON file"),
                              aidoc_id: str,
                              db: Session = Depends(deps.get_db),
                              _: str = Depends(auth.validate_user_token)
                              ) -> Any:
    """
    Upload the qc1 protocol xml file
    """
    try:
        metadata_resource = crud.pd_protocol_metadata.get(db, id = aidoc_id)

        if metadata_resource is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Document found for {aidoc_id}")

        # Save the file
        target_folder = Path(metadata_resource.documentFilePath).parent
        target_abs_filename = Path(target_folder, f"{config.QC_WIP_SRC_QC_FILE_PREFIX}_{aidoc_id}.json")
        validate_qc_protocol_file(uploaded_json_file.content_type) # validate uploaded file type
        saved_file_details = save_json_file(target_folder=target_folder, target_abs_filename = target_abs_filename, uploaded_file=uploaded_json_file)

        # Save file contents to DB
        _ = crud.pd_protocol_qcdata.save_qc_jsondata_to_db(db, aidoc_id, saved_file_details.get("target_abs_filename"))

        # Extract DB contents to file
        db_resource, _ = crud.pd_protocol_qcdata.save_db_jsondata_to_file(db = db, aidoc_id = aidoc_id, file_prefix=config.QC_WIP_SRC_DB_FILE_PREFIX)
        return db_resource
    except Exception as exc:
        logger.exception(f'pd-ui-backend: Exception occured in qc_protocol_upload {str(exc)}')
        raise exc
