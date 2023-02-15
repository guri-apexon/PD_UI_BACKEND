from typing import Any, List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app import qc_ingest, schemas
from app.api import deps
from app.api.endpoints import auth
from app.qc_ingest import qc_ingest_service

router = APIRouter()


@router.post("/")
async def qc_ingest(
        *,
        payload: list,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    payload for qc_ingest text
    """
    try:
        result = qc_ingest_service.process(payload)
        return_responce = {"success": result}
        if result is True:
            return_responce["message"] = "QC ingest Completed Successfully"
        else:
            return_responce["message"] = "QC ingest failed"
        return return_responce
    except Exception as ex:
        raise HTTPException(
            detail=f"Exception occurred while qc ingest running: {str(ex)}")
