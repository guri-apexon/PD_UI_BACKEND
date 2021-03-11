import logging
import os
from typing import Any

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import crud, schemas
from app.api import deps
from app.utilities.config import settings
from app.utilities.file_utils import validate_qc_protocol_file, save_request_file

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)


@router.get("/", response_model=schemas.ProtocolData)
def get_protocol_data(
        db: Session = Depends(deps.get_db),
        id: str = "id",
) -> Any:
    """
    Get protocol data.
    """
    protocol_data = crud.pd_protocol_data.get(db, id)
    return protocol_data


@router.get("/qc", response_model=schemas.ProtocolData)
def get_protocol_data(
        db: Session = Depends(deps.get_db),
        id: str = "id",
) -> Any:
    """
    Get protocol data.
    """
    protocol_data = crud.pd_protocol_data.get_inactive_record(db, id)
    return protocol_data


@router.get("/qc1_protocol_review_json")
def download_qc1_protocol_data_json(
        aidoc_id: str = None,
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
                              ) -> Any:
    """
    Upload the qc1 protocol xml file
    """
    try:
        protocol_data_updation_status = ""
        aidoc_id = aidoc_id
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


@router.put("/qc_approve", response_model=bool)
def read_protocol_metadata(
        db: Session = Depends(deps.get_db),
        aidoc_id: str = None,
) -> Any:
    """
    Retrieve all Protocol Sponsors.
    """
    if aidoc_id is not None:
        try:
            crud.pd_protocol_data.qc_approve(db, aidoc_id)
            return True
        except Exception as ex:
            logger.exception(f'pd-ui-backend: Exception occured in qc_approve {str(ex)}')
            raise HTTPException(status_code=403, detail=f'Exception occured in qc_approve {str(ex)}')
    else:
        logger.exception(f'pd-ui-backend: Exception occured - no aidoc_id provided')
        raise HTTPException(status_code=404, detail="No aidoc_id provided.")
