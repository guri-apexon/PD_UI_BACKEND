import logging
from typing import Any, List

from app import config, crud, schemas
from app.api import deps
from app.schemas.pd_protocol_metadata import ProtocolMetadataUserId, ChangeQcStatus
from app.utilities import utils
from app.utilities.config import settings
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.utilities.file_utils import post_qc_approval_complete_to_mgmt_service

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)


@router.get("/", response_model = List[ProtocolMetadataUserId])
async def read_protocol_metadata(*,
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
            protocol_metadata = await crud.pd_protocol_metadata.get_by_doc_id(db, id = doc_id_input)
        
        elif user_id_input in config.VALID_QC_STATUS:
            protocol_metadata = await crud.pd_protocol_metadata.get_qc_protocols(db, user_id_input)

        else:
            protocol_metadata = await crud.pd_protocol_metadata.get_metadata_by_userId(db, user_id_input)

        # Enrich with QC data for all documents
        for idx, doc_row_dict in enumerate(protocol_metadata):
            logger.debug(f"Metadata QC update check for id: {doc_row_dict['id']}")
            doc_row_dict = await utils.update_qc_fields(pd_attributes_for_dashboard = doc_row_dict, \
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
    Create a new protocol
    """
    protocol_metadata = crud.pd_protocol_metadata.create(db, obj_in=protocol_metadata_in)
    return protocol_metadata


@router.put("/activate_protocol", response_model=bool)
def activate_protocol(
        db: Session = Depends(deps.get_db),
        aidoc_id: str = None,
) -> Any:
    """
    Activate protocol document
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


@router.put("/change_qc_status")
async def change_qc_status(*, db: Session = Depends(deps.get_db), 
            request_body: ChangeQcStatus) -> Any:
    """
    Change QC status of requested document ids
    """
    response_dict = dict()
    all_success = True
    doc_id_array = request_body.docIdArray
    target_status = request_body.targetStatus
    try:
        for aidocid in doc_id_array:
            aidocid = aidocid.strip()

            update_status, message_str = await crud.pd_protocol_metadata.change_qc_status(db, doc_id = aidocid, target_status = target_status)
            response_dict[aidocid] = {'is_success': update_status, 'message': message_str}
            all_success &= update_status
        
        logger.debug(f"all_success: {all_success}, response: {response_dict}")
        return {'all_success': all_success, 'response': response_dict}
    except Exception as exc:
        logger.exception(f"Exception received which changing QC status. Exception: {str(exc)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(exc)}")


@router.put("/qc_approve", response_model=bool)
async def approve_qc(
        db: Session = Depends(deps.get_db),
        aidoc_id: str = Query(..., description = "Internal document id", min_length = 1),
        approvedBy: str = Query(..., description = "Approved UserId", min_length = 1)
) -> Any:
    """
    Perform following activities once the QC activity is completed and approved:
        * Mark qcStatus as complete
        * Ask mgmt svc API to insert/update qc_summary table with updated details (SRC='QC')
        * Update elastic search with latest details
    """
    qc_status_update_flg = False

    try:
        # Make a post call to management service end point for post-qc process
        mgmt_svc_flg = await post_qc_approval_complete_to_mgmt_service(aidoc_id, approvedBy)

        # Update elastic search
        update_es_res = crud.qc_update_elastic(aidoc_id, db)

        # Update qcStatus
        if update_es_res['ResponseCode'] == status.HTTP_200_OK and mgmt_svc_flg:
            qc_status_update_flg, _ = await crud.pd_protocol_metadata.change_qc_status(db, doc_id = aidoc_id, target_status = config.QC_COMPLETED_STATUS)
            logger.debug(f"change_qc_status returned with {qc_status_update_flg}")

        if qc_status_update_flg:
            logger.info(f'{aidoc_id}: qc_approve completed successfully')
            return True
        else:
            logger.error(f"""{aidoc_id}: qc_approve did NOT completed successfully. \
                            \nqc_status_update_flg={qc_status_update_flg}; mgmt_svc_flg={mgmt_svc_flg}; ES_update_flg={update_es_res['ResponseCode']}; """)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"""{aidoc_id}: qc_approve did NOT completed successfully. \
                            \nqc_status_update_flg={qc_status_update_flg}; mgmt_svc_flg={mgmt_svc_flg}; ES_update_flg={update_es_res['ResponseCode']}; """)
    except Exception as ex:
        logger.exception(f'{aidoc_id}: Exception occurred in qc_approve {str(ex)}')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Exception occurred in qc_approve {str(ex)}')
