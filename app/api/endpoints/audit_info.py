from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from app.api.endpoints import auth
from app.qc_ingest import audit_info_service

router = APIRouter()


@router.get("/get_audit_info")
async def get_audit_info(
        *,
        type: str = "",
        line_id: str = "",
        doc_id: str = "",
        link_id: str = "",
        link_id_level2: str = "",
        link_id_level3: str = "",
        link_id_level4: str = "",
        link_id_level5: str = "",
        link_id_level6: str = "",
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    payload for get method of audit info
    """
    try:
        payload = {"type": type,
                    "line_id": line_id,
                    "doc_id": doc_id,
                    "link_id": link_id,
                    "link_id_level2": link_id_level2,
                    "link_id_level3": link_id_level3,
                    "link_id_level4": link_id_level4,
                    "link_id_level5": link_id_level5,
                    "link_id_level6": link_id_level6}
        result = audit_info_service.get(payload)
        return {"success": True,"info":result}
    except Exception as ex:
        raise HTTPException(status_code=400,
                            detail=f"Exception occurred audit info GET method: {str(ex)}")

