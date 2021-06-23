import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas, config
from app.api import deps
from app.api.endpoints.protocol_attributes import read_protocol_attributes
from app.utilities.config import settings
from app.utilities import utils

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)


@router.get("/")
def read_protocol_metadata(
        userId: str,
        getQcInprogressAttr: bool = False,
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Retrieve Protocol metadata associated with the user
    """
    user_input = userId.strip()
    protocol_metadata = []
    logger.debug(f'read_protocol_metadata: Getting Metadata for the userID {user_input}')
    
    if user_input is None:
        logger.exception(f'read_protocol_metadata: No Input Provided')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Input provided.")

    try:
        if user_input in config.qc_status_all:
            protocol_metadata = crud.pd_protocol_metadata.get_qc_protocols(db, user_input)

        else:
            protocol_metadata = crud.pd_protocol_metadata.get_metadata_by_userId(db, user_input)

        # Enrich with QC data for all entries
        for idx, doc_row_dict in enumerate(protocol_metadata):
            logger.debug(f"Metadata QC update check for id: {doc_row_dict['id']}")
            doc_row_dict['amendmentNumber'] = None # Only present in QC record
            doc_row_dict['approvalDate'] = doc_row_dict['approvalDate'].strftime('%Y-%m-%d') if doc_row_dict['approvalDate'] is not None else None
            
            doc_row_dict = utils.update_qc_fields(pd_attributes_for_dashboard = doc_row_dict, \
                                    get_qc_inprogress_attr_flg = getQcInprogressAttr, db = db)
            protocol_metadata[idx] = doc_row_dict

    except Exception as ex:
        logger.exception(f'read_protocol_metadata: Exception occured in read_protocol_metadata {str(ex)}')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Exception occured in read_protocol_metadata {str(ex)}')
    return protocol_metadata


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
