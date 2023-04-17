from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException
from app.api.endpoints import auth
from app.qc_ingest import section_lock_service

router = APIRouter()


@router.get("/get_section_lock")
async def get_section_lock(
        *,
        link_id: str,
        doc_id: str,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    payload for get method of section lock
    """
    try:
        result = section_lock_service.get({"link_id": link_id, "doc_id": doc_id})
        return {"success": True,"info":result}
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
        return {"success": True,"info":result}
    except Exception as ex:
        raise HTTPException(status_code=500,
                            detail=f"Exception occurred section lock PUT method: {str(ex)}")

@router.post("/submit_protocol_workflow")
async def SubmitProtocolWorkflow(
        *,
        payload: dict,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    payload for delete of section lock and call workflow run
    """
    try:
        result = section_lock_service.remove(payload)
        return {"success": True,"info":result}
    except Exception as ex:
        raise HTTPException(status_code=500,
                            detail=f"Exception occurred section lock delete: {str(ex)}")


@router.get("/document_lock_status")
async def get_document_lock_status(
        *,
        user_id: str,
        doc_id: str,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    API for getting document lock status
    """
    try:
        result = section_lock_service.get_document_lock_status({"doc_id": doc_id, "user_id": user_id})
        return {"document_lock_status": True} if result else {"document_lock_status": False}
    except Exception as ex:
        raise HTTPException(status_code=500,
                            detail=f"Exception occurred document lock status: {str(ex)}")
