from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=schemas.ProtocolLatestRecord)
def read_protocol_mcra(
        db: Session = Depends(deps.get_db),
        protocol: str = None,
        versionNumber: str = None,
) -> Any:
    """
    Retrieve latest protocol document.
    """
    mcra = crud.pd_protocol_metadata.get_latest_protocol(db, protocol, versionNumber)
    return mcra

