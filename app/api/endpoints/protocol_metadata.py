import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.api.endpoints.protocol_attributes import read_protocol_attributes
from app.utilities.config import settings

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)


@router.get("/")
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
                logger.exception(f'pd-ui-backend: Exception occured in read_protocol_metadata {str(ex)}')
                raise HTTPException(status_code=403, detail=f'Exception occured {str(ex)}')
        else:
            try:
                protocol_metadata = []
                aidoc_id_list = []
                logger.debug(f'pd-ui-backend: Getting Metadata for the userID {userId}')
                protocol_metadata_aidoc_ids = crud.pd_protocol_metadata.get_metadata_by_userId(db, userId)
                if protocol_metadata_aidoc_ids is not None:
                    # Get the list of all aidoc-ids for the given userID with the earlier logic
                    for ele in range(len(protocol_metadata_aidoc_ids)):
                        aidoc_id_list.append(protocol_metadata_aidoc_ids[ele][0])
                    # Call the protocol_attributes updated method with all the list of aidoc-ids
                    for aidoc_id in aidoc_id_list:
                        logger.debug(f'pd-ui-backend: Getting Metadata to the aidocId: {aidoc_id} for userId: {userId}')
                        protocol_metadata.append(read_protocol_attributes(db, aidoc_id))
            except Exception as ex:
                logger.exception(f'pd-ui-backend: Exception occured in read_protocol_metadata {str(ex)}')
                raise HTTPException(status_code=403, detail=f'Exception occured in read_protocol_metadata {str(ex)}')
        return protocol_metadata
    else:
        logger.exception(f'pd-ui-backend: No Input Provided')
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
def activate_protocol(
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
            logger.exception(f'pd-ui-backend: Exception occured in activate_protocol {str(ex)}')
            raise HTTPException(status_code=403, detail=f'Exception occured {str(ex)}')
    else:
        logger.exception("pd-ui-backend: No aidoc_id provided in input")
        raise HTTPException(status_code=404, detail="No aidoc_id provided.")


@router.put("/qc1_to_qc2", response_model=bool)
def change_qc1_to_qc2(
        db: Session = Depends(deps.get_db),
        aidoc_id: str = None,
) -> Any:
    """
    Retrieve all Protocol Sponsors.
    """
    if aidoc_id is not None:
        try:
            protocol_metadata = crud.pd_protocol_metadata.qc1_to_qc2(db, aidoc_id)
            return protocol_metadata
        except Exception as ex:
            logger.exception(f'pd-ui-backend: Exception occured in change QC1 to QC2 {str(ex)}')
            raise HTTPException(status_code=403, detail=f'Exception occured {str(ex)}')
    else:
        logger.exception("pd-ui-backend: No aidoc_id provided in input")
        raise HTTPException(status_code=404, detail="No aidoc_id provided.")


@router.put("/qc_reject", response_model=bool)
def qc_reject(
        db: Session = Depends(deps.get_db),
        aidoc_id: str = None,
) -> Any:
    """
    Retrieve all Protocol Sponsors.
    """
    if aidoc_id is not None:
        try:
            protocol_metadata = crud.pd_protocol_metadata.qc_reject(db, aidoc_id)
            return protocol_metadata
        except Exception as ex:
            logger.exception(f'pd-ui-backend: Exception occured in change QC Reject {str(ex)}')
            raise HTTPException(status_code=403, detail=f'Exception occured {str(ex)}')
    else:
        logger.exception("pd-ui-backend: No aidoc_id provided in input")
        raise HTTPException(status_code=404, detail="No aidoc_id provided.")
