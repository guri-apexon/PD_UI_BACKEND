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
from app.utilities.file_utils import save_bulkmap_file
from app.api.endpoints import auth

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)

@router.post("/user_protocol_many")
def add_user_protocol_many_to_many(*, user_protocol_xls_file: UploadFile = File(..., description="Upload User_Protocol Excel File(.xlsx)")
                                   ,db: Session = Depends(deps.get_db),
                              _: str = Depends(auth.validate_user_token)) -> Any:
    try:
        user_protocol_path = save_bulkmap_file(user_protocol_xls_file)
        user_protocol_updation_status = crud.pd_user_protocols.excel_data_to_db(db, user_protocol_path)
        if user_protocol_updation_status==False:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                                detail="Invalid File Type Received, Please Provide Excel(.xlsx) file only")
        else:
            return user_protocol_updation_status

    except Exception as ex:
        logger.exception(f'pd-ui-backend: Exception occured in qc_protocol_upload {str(ex)}')
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail="Invalid file received, please provide excel file(.xlsx) or Excel file may not contain data" + str(ex))