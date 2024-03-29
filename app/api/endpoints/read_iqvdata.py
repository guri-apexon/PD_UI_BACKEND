from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.api.endpoints import auth

router = APIRouter()


@router.get("/", response_model=schemas.ProtocolDataReadIqvdata)
def get_protocol_data(
        db: Session = Depends(deps.get_db),
        id: str = "id",
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Get protocol data.
    """
    protocol_data = crud.pd_protocol_data.get(db, id)
    return protocol_data

@router.post("/", response_model=schemas.ProtocolData)
def create_iqvdata(
        *,
        db: Session = Depends(deps.get_db),
        protocol_data_in: schemas.ProtocolDataCreate,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Create a post status.
    """
    protocol_data = crud.pd_protocol_data.create(db, obj_in=protocol_data_in)
    return protocol_data
