import logging
from datetime import datetime
from pathlib import Path
from typing import Any, List

from app import config, crud, schemas
from app.api import deps
from app.api.endpoints import auth
from app.schemas.pd_protocol_metadata import (ChangeQcStatus,
                                              ProtocolMetadataUserId)
from app.utilities import file_utils, utils
from app.utilities.config import settings
from app.utilities.elastic_utilities import update_elastic
from app.utilities.file_utils import post_qc_approval_complete_to_mgmt_service
from app.utilities.redact import redactor
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)


@router.get("/", response_model = List[ProtocolMetadataUserId])
async def read_protocol_metadata(*,
        db: Session = Depends(deps.get_db),
        userId: str = Query(None, description = 'UserId associated with the document(s)', min_length=3, max_length=30),
        docId: str = Query(None, description = 'Internal document id', min_length=10, max_length=50),
        getQcInprogressAttr: bool = Query(False, description = 'Override flag to get QC data which are in-progress'),
        _: str = Depends(auth.validate_user_token)
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
            protocol_metadata = await crud.pd_protocol_metadata.get_by_doc_id(db, id=doc_id_input, user_id=user_id_input)
        
        elif user_id_input in config.VALID_QC_STATUS:
            protocol_metadata = await crud.pd_protocol_metadata.get_qc_protocols(db, user_id_input)

        else:
            protocol_metadata = await crud.pd_protocol_metadata.get_metadata_by_userId(db, user_id_input)

        # Enrich with QC data for all documents
        for idx, doc_row_dict in enumerate(protocol_metadata):
            doc_row_dict = await utils.update_qc_fields(pd_attributes_for_dashboard=doc_row_dict,
                                                        get_qc_inprogress_attr_flg=getQcInprogressAttr,
                                                        db=db)
            if userId not in ["QC1", "QC2"]:
                _, doc_row_dict = redactor.on_attributes(current_db=db, multiple_doc_attributes=[doc_row_dict])
            protocol_metadata[idx] = doc_row_dict

    except Exception as ex:
        logger.exception(f'read_protocol_metadata: Exception occurred in read_protocol_metadata {str(ex)}')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Exception occurred in read_protocol_metadata {str(ex)}')
    return protocol_metadata


@router.post("/", response_model=schemas.ProtocolMetadata)
def create_protocol_metadata(
        *,
        db: Session = Depends(deps.get_db),
        protocol_metadata_in: schemas.ProtocolMetadataCreate,
        _: str = Depends(auth.validate_user_token)
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
        _: str = Depends(auth.validate_user_token)
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
            request_body: ChangeQcStatus, _: str = Depends(auth.validate_user_token)) -> Any:
    """
    Change QC status of requested document ids
    """
    response_dict = dict()
    all_success = True
    current_timestamp = datetime.utcnow()
    current_utc_num_format = current_timestamp.strftime("%Y%m%d%H%M%S")
    doc_id_array = request_body.docIdArray
    target_status = request_body.targetStatus
    try:
        for aidocid in doc_id_array:
            # Update in DB
            db_update_status, db_message_str = await crud.pd_protocol_metadata.change_qc_status(db, doc_id = aidocid, target_status = target_status, 
                                                                                                    current_timestamp = current_timestamp)

            # Update in ES
            es_qc_status_update_dict = {'qcStatus': target_status, 'TimeUpdated': current_utc_num_format}
            es_response = update_elastic({'doc' : es_qc_status_update_dict}, aidocid)

            if es_response:
                es_message_str = ". ES update completed"
                es_update_status = True
            else:
                es_message_str = ". ES update failed"
                es_update_status = False

            message_str = db_message_str + es_message_str
            if not es_update_status or not db_update_status:
                response_dict[aidocid] = {'is_success': False, 'message': message_str}
                all_success = False
            else:
                response_dict[aidocid] = {'is_success': True, 'message': message_str}
     
        logger.debug(f"all_success: {all_success}, response: {response_dict}")
        return {'all_success': all_success, 'response': response_dict}
    except Exception as exc:
        logger.exception(f"Exception received which changing QC status. Exception: {str(exc)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(exc)}")


@router.put("/qc_approve", response_model=bool)
async def approve_qc(
        db: Session = Depends(deps.get_db),
        aidoc_id: str = Query(..., description = "Internal document id", min_length = 1),
        approvedBy: str = Query(..., description = "Approved UserId", min_length = 1),
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Perform following activities once the QC activity is completed and approved:
        * Create QC file
        * Create DIG file
        * Initiate mgmt svc API to insert/update qc_summary table with updated details (SRC='QC'), setup for Feedback RUN
    """
    qc_filename = None

    try:
        # Get current state
        metadata_resource = crud.pd_protocol_metadata.get_by_id(db, id = aidoc_id)
        if not metadata_resource:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"No Document found for {aidoc_id}")

        run_prefix = "R" + str(metadata_resource.runId).zfill(2)

        # Create QC file
        qc_file_prefix = run_prefix + config.QC_APPROVED_FILE_PREFIX
        qc_file_flg, target_abs_filename = file_utils.rename_json_file(db, aidoc_id = aidoc_id, src_prefix=config.QC_WIP_SRC_DB_FILE_PREFIX, target_prefix=qc_file_prefix)

        if not qc_file_flg:
            _, qc_filename = crud.pd_protocol_qcdata.save_db_jsondata_to_file(db, aidoc_id=aidoc_id, file_prefix=qc_file_prefix)
            qc_file_flg = True if qc_filename is not None else False

        # Create DIG file															
        dig_file_prefix = run_prefix + config.DIG_FILE_PREFIX															
        target_folder = Path(metadata_resource.documentFilePath).parent															
        dig_saved_filename = crud.pd_protocol_data.save_db_jsondata_to_dig_file(db, aidoc_id=aidoc_id, target_folder=target_folder, file_prefix=dig_file_prefix)															
        logger.debug(f"dig_saved_filename: {dig_saved_filename}")															


        # Make a post call to management service end point for post-qc process
        if qc_file_flg:
            parent_path = target_abs_filename.parent
            mgmt_svc_flg = await post_qc_approval_complete_to_mgmt_service(aidoc_id, approvedBy, parent_path)

        if qc_file_flg and dig_saved_filename and mgmt_svc_flg:
            logger.info(f'{aidoc_id}: qc_approve completed successfully')
            return True
        else:
            logger.error(f"""{aidoc_id}: qc_approve did NOT completed successfully. \
                            \nrename_flg={qc_file_flg}; mgmt_svc_flg={mgmt_svc_flg};  dig_saved_filename={dig_saved_filename}""")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"""{aidoc_id}: qc_approve did NOT completed successfully. \
                            \nrename_flg={qc_file_flg}; mgmt_svc_flg={mgmt_svc_flg};  dig_saved_filename={dig_saved_filename}""")
    except Exception as ex:
        logger.exception(f'{aidoc_id}: Exception occurred in qc_approve {str(ex)}')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Exception occurred in qc_approve {str(ex)}')
