from typing import Any, List

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app import qc_ingest, schemas
from app.api import deps
from app.api.endpoints import auth
from app.qc_ingest import QC_ingest, QC_ingest_image
import json

router = APIRouter()

@router.post("/qc_ingest_text")
async def qc_ingest_text(
        *,
        payload: list,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    payload for qc_ingest text
    """
    try:
        result = qc_ingest.QC_ingest.process(payload)
        if result is True:
            return "QC ingest Completed Successfully for text data"
        else:
            return "QC ingest failed for text"
    except Exception as ex:
        raise HTTPException(detail=f"Exception occurred while qc ingest running for text: {str(ex)}")

@router.post("/qc_ingest_image")
async def qc_ingest_image(
        *,
        payload: list,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    payload for qc_ingest image
    """
    try:
        result = qc_ingest.QC_ingest_image.process(payload)
        if result is True:
            return "QC ingest Completed Successfully for image data"
        else:
            return "QC ingest failed for image"
    except Exception as ex:
        raise HTTPException(detail=f"Exception occurred while qc ingest running for image: {str(ex)}")

@router.post("/qc_ingest_table")
async def qc_ingest_table(
        *,
        payload: list,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    payload for qc_ingest table
    """
    try:
        result = qc_ingest.QC_ingest_table.process(payload)
        if result is True:
            return "QC ingest Completed Successfully for table data"
        else:
            return "QC ingest failed for table"
    except Exception as ex:
        raise HTTPException(detail=f"Exception occurred while qc ingest running for table: {str(ex)}")
