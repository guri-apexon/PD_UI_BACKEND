from typing import Any, List
from starlette import status

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.utilities.file_utils import validate_xml_file, save_request_file

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


@router.get("/qc1_protocol_review")
def read_qc2_protocols(
        db: Session = Depends(deps.get_db),
        aidoc_id: str = None,
) -> Any:
    """
    Retrieve all Protocol Sponsors.
    """
    iqvdata_xlsx_file_path = crud.pd_protocol_data.generate_iqvdata_xlsx_file(db, aidoc_id)
    return iqvdata_xlsx_file_path


@router.post("/qc1_protocol_upload")
async def qc1_protocol_upload(*,
                              iqvdata_xls_file: UploadFile = File(..., title="Updated IQVData Excel File",
                                                                  description="Upload Updated Excel file"),
                              aidoc_id: str,
                              db: Session = Depends(deps.get_db),
                              ) -> Any:
    """
    Upload the qc1 protocol xml file
    """
    try:
        aidoc_id = aidoc_id
        protocol_file_path = save_request_file(aidoc_id, iqvdata_xls_file)['file_path']
        validate_xml_file(aidoc_id, iqvdata_xls_file.content_type)
        # TODO: Read the contents of the uploaded excel file and push to DB in the following 3 columns
        # 1. iqvdataToc_QC
        # 2. iqvdataSoa_QC
        # 3. iqvdataSummary_QC
        protocol_data_updation_status = crud.pd_protocol_data.save_qc_data_to_db(db, aidoc_id, protocol_file_path)
        return protocol_data_updation_status
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail="Invalid Source/Target file received" + str(ex))

