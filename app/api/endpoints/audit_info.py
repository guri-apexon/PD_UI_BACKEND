from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from app.api.endpoints import auth
from app.qc_ingest import audit_info_service

router = APIRouter()


@router.get("/get_audit_info")
async def get_audit_info(
        *,
        payload: dict,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    payload for get method of audit info
    """
    try:
        result = audit_info_service.get(payload)
        return result
    except Exception as ex:
        raise HTTPException(status_code=500,
                            detail=f"Exception occurred audit info GET method: {str(ex)}")

