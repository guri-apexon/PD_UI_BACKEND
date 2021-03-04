from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.ProtocolMetadata])
def read_protocol_metadata(
        db: Session = Depends(deps.get_db),
        userId: str = None,
) -> Any:
    """
    Retrieve all Protocol Sponsors.
    """
    user_input = userId
    if user_input is not None:
        if user_input == "QC1" or user_input == "QC2":
            try:
                protocol_metadata = crud.pd_protocol_metadata.get_qc_protocols(db, userId)
            except Exception as ex:
                raise HTTPException(status_code=403, detail=f'Exception occured {ex}')
        else:
            try:
                protocol_metadata = crud.pd_protocol_metadata.get_metadata_by_userId(db, userId)
            except Exception as ex:
                raise HTTPException(status_code=403, detail=f'Exception occured {ex}')
        return protocol_metadata
    else:
        raise HTTPException(status_code=404, detail="No Input provided.")


@router.post("/", response_model=schemas.ProtocolMetadata)
def create_protocol_metadata(
        *,
        db: Session = Depends(deps.get_db),
        protocol_metadata_in: schemas.ProtocolMetadataCreate,
) -> Any:
    """
    Create a new protocol sponsor.
    """
    protocol_metadata = crud.pd_protocol_metadata.create(db, obj_in=protocol_metadata_in)
    return protocol_metadata


@router.put("/activate_protocol", response_model=bool)
def read_protocol_metadata(
        db: Session = Depends(deps.get_db),
        aidoc_id: str = None,
) -> Any:
    """
    Retrieve all Protocol Sponsors.
    """
    if aidoc_id is not None:
        try:
            protocol_metadata = crud.pd_protocol_metadata.activate_protocol(db, aidoc_id)
            return protocol_metadata
        except Exception as ex:
            raise HTTPException(status_code=403, detail=f'Exception occured {ex}')
    else:
        raise HTTPException(status_code=404, detail="No aidoc_id provided.")
