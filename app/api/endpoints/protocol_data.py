import logging
import os
from typing import Any

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from app import crud, schemas, config
from app.api import deps
from app.utilities.config import settings
from app import crud
from app.utilities.file_utils import validate_qc_protocol_file, save_request_file, \
    post_qc_approval_complete_to_mgmt_service

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)


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


@router.get("/qc", response_model=schemas.ProtocolData)
def get_protocol_data(
        db: Session = Depends(deps.get_db),
        id: str = "id",
) -> Any:
    """
    Get protocol data.
    """
    protocol_data = crud.pd_protocol_data.get_inactive_record(db, id)
    return protocol_data


@router.get("/qc1_protocol_review_json")
def download_qc1_protocol_data_json(
        aidoc_id: str = None,
) -> Any:
    """
    Retrieve all Protocol Sponsors.
    """
    try:
        iqvdata_json_file_path = crud.pd_protocol_data.generate_iqvdata_json_file(aidoc_id)
        return iqvdata_json_file_path
    except Exception as ex:
        logger.exception(f'pd-ui-backend: Exception occured in qc-protocol-data-json download {str(ex)}')
        raise HTTPException(status_code=401, detail=f"Exception in qc-protocol-data-json download {str(ex)}")


@router.get("/qc1_protocol_review_xlsx")
def download_qc1_protocol_data_xlsx(
        aidoc_id: str = None,
) -> Any:
    """
    Retrieve all Protocol Sponsors.
    """
    try:
        iqvdata_xlsx_file_path = crud.pd_protocol_data.generate_iqvdata_xlsx_file(aidoc_id)
        return iqvdata_xlsx_file_path
    except Exception as ex:
        logger.exception(f'pd-ui-backend: Exception occured in qc-protocol-data-xlsx download {str(ex)}')
        raise HTTPException(status_code=401, detail=f"Exception in qc-protocol-data-xlsx download {str(ex)}")


@router.post("/qc1_protocol_upload")
async def qc1_protocol_upload(*,
                              iqvdata_xls_file: UploadFile = File(..., title="Updated IQVData JSON file",
                                                                  description="Upload Updated JSON file"),
                              aidoc_id: str,
                              db: Session = Depends(deps.get_db),
                              ) -> Any:
    """
    Upload the qc1 protocol xml file
    """
    try:
        protocol_data_updation_status = ""
        aidoc_id = aidoc_id
        protocol_file_path = save_request_file(aidoc_id, iqvdata_xls_file)['file_path']
        validate_qc_protocol_file(iqvdata_xls_file.content_type)

        uploaded_file_name_split = os.path.splitext(protocol_file_path)

        if uploaded_file_name_split[1] == ".json":
            protocol_data_updation_status = crud.pd_protocol_data.save_qc_jsondata_to_db(db, aidoc_id,
                                                                                         protocol_file_path)
        elif uploaded_file_name_split[1] == ".xlsx":
            protocol_data_updation_status = crud.pd_protocol_data.save_qc_exceldata_to_db(db, aidoc_id,
                                                                                          protocol_file_path)
        return protocol_data_updation_status
    except Exception as ex:
        logger.exception(f'pd-ui-backend: Exception occured in qc_protocol_upload {str(ex)}')
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail="Invalid Source/Target file received" + str(ex))


@router.put("/qc_approve", response_model=bool)
async def approved_qc(
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
    try:
        # Update qcStatus
        qc_status_update_flg, _ = await crud.pd_protocol_metadata.change_qc_status(db, doc_id = aidoc_id, target_status = config.QC_COMPLETED_STATUS)
        logger.debug(f"change_qc_status returned with {qc_status_update_flg}")
        
        # Make a post call to management service end point for post-qc process
        mgmt_svc_flg = await post_qc_approval_complete_to_mgmt_service(aidoc_id, approvedBy)

        # Update elastic search
        update_es_res = crud.qc_update_elastic(aidoc_id, db)

        if qc_status_update_flg and mgmt_svc_flg and update_es_res['ResponseCode'] == status.HTTP_200_OK:
            logger.info(f'{aidoc_id}: qc_approve completed successfully')
            return True
        else:
            logger.error(f"""{aidoc_id}: qc_approve did NOT completed successfully. \
                            \nqc_status_update_flg={qc_status_update_flg}; mgmt_svc_flg={mgmt_svc_flg}; ES_update_flg={update_es_res['ResponseCode']}; """)
            return False
    except Exception as ex:
        logger.exception(f'{aidoc_id}: Exception occurred in qc_approve {str(ex)}')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Exception occurred in qc_approve {str(ex)}')
