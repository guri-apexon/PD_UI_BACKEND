from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException
from app.api.endpoints import auth
from app.qc_ingest import section_lock_service

router = APIRouter()


@router.get("/get_section_lock")
async def get_section_lock(
        *,
        payload: dict,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    payload for get method of section lock
    """
    try:
        result = section_lock_service.get(payload)
        return result
    except Exception as ex:
        raise HTTPException(status_code=500,
                            detail=f"Exception occurred section lock GET method: {str(ex)}")


@router.put("/put_section_lock")
async def put_section_lock(
        *,
        payload: dict,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    payload for put method of section lock
    """
    try:
        result = section_lock_service.put(payload)
        return result
    except Exception as ex:
        raise HTTPException(status_code=500,
                            detail=f"Exception occurred section lock PUT method: {str(ex)}")