from typing import Any, List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app import qc_ingest, schemas
from app.api import deps
from app.api.endpoints import auth
from app.qc_ingest import qc_ingest_service
from app.utilities.utils import notification_service
import logging
from app.utilities.config import settings

logger = logging.getLogger(settings.LOGGER_NAME)

router = APIRouter()


@router.post("/")
async def qc_ingest(
        *,
        doc_id: str,
        payload: list,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    payload for qc_ingest text
    """
    try:
        result = qc_ingest_service.process(payload)

        # adding edited notification service function call
        try:
            notification_service(doc_id, "EDITED",False)
            logger.info(f"Edited event notification records successfully created for doc_id {doc_id}")
        except Exception as ex:
            logger.exception(f"exception occured for doc_id {doc_id} to edited event notifications : {str(ex)}")
        
        return {"success": True,"message":"QC ingest Completed Successfully","info":result}
    except Exception as ex:
        raise HTTPException(status_code=500,
            detail=f"Exception occurred while qc ingest running: {str(ex)}")
