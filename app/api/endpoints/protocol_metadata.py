import logging
from typing import Any, List

from app import config, crud, schemas
from app.api import deps
from app.schemas.pd_protocol_metadata import ProtocolMetadataUserId
from app.utilities import utils
from app.utilities.config import settings
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)


@router.get("/", response_model = List[ProtocolMetadataUserId])
def read_protocol_metadata(*,
        db: Session = Depends(deps.get_db),
        userId: str = Query(None, description = 'UserId associated with the document(s)', min_length=3, max_length=30),
        docId: str = Query(None, description = 'Internal document id', min_length=10, max_length=50),
        getQcInprogressAttr: bool = Query(False, description = 'Override flag to get QC data which are in-progress')
) -> Any:
    """
    Retrieves Protocol metadata of all the documents associated with the requested userId or docId
    > Note: If both userId and docId are provided, only docId is considered
    """
    user_id_input = userId.strip() if userId is not None else userId
    doc_id_input = docId.strip() if docId is not None else docId

    protocol_metadata = []
    logger.debug(f'read_protocol_metadata: Getting Metadata for the userID:{user_id_input} or doc_id:{doc_id_input}')
    
    if user_id_input is None and doc_id_input is None:
        logger.exception(f'read_protocol_metadata: No Valid input Provided')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Valid input Provided")

    try:
        if doc_id_input is not None:
            protocol_metadata = crud.pd_protocol_metadata.get_by_doc_id(db, id = doc_id_input)
        
        elif user_id_input in config.VALID_QC_STATUS:
            protocol_metadata = crud.pd_protocol_metadata.get_qc_protocols(db, user_id_input)

        else:
            protocol_metadata = crud.pd_protocol_metadata.get_metadata_by_userId(db, user_id_input)

        # Enrich with QC data for all documents
        for idx, doc_row_dict in enumerate(protocol_metadata):
            logger.debug(f"Metadata QC update check for id: {doc_row_dict['id']}")
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
