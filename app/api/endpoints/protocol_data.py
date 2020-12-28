from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


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


