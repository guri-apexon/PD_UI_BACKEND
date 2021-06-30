import json
import requests
import logging
import os
import shutil
from pathlib import Path

import pandas as pd
from fastapi import UploadFile, HTTPException
from starlette import status

from app.utilities.config import settings

logger = logging.getLogger(settings.LOGGER_NAME)


def save_request_file(_id, upload_file: UploadFile):
    """
    Saves the request files in the processing folder
    """
    req_dir = Path(settings.PROCESSING_DIR, 'qc_uploads')
    if not req_dir.is_dir():
        req_dir.mkdir()

    file_path = Path(req_dir, upload_file.filename)
    if Path(req_dir).is_dir():
        try:
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(upload_file.file, buffer)
        finally:
            upload_file.file.close()

    if file_path.is_file() and req_dir.is_dir():
        return {'file_path': file_path, 'file_dir': req_dir}
    else:
        raise FileNotFoundError("The Uploaded file was not been saved properly, please try again")


def validate_qc_protocol_file(file_content_type: str,
                              ):
    """
    Validates the Uploaded file type content before processing
    """
    if not (file_content_type in ['application/json']):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Invalid File Format - only json file will be accepted",
        )


def write_data_to_json(aidoc_id: str, data: str):
    try:
        json_object = json.dumps(data, indent=4)
        json_file_name = os.path.join(settings.PROCESSING_DIR, aidoc_id + ".json")
        with open(json_file_name, "w") as outfile:
            outfile.write(json_object)
        logger.info("Writing data to JSON file completed")
        return json_file_name
    except Exception as ex:
        logger.exception(f"Exception occured in writing Data to JSON file {str(ex)}")
        raise HTTPException(status_code=401, detail=f"Exception occured in writing data to JSON file {str(ex)}")


def write_data_to_xlsx(aidoc_id: str, data: str):
    """
    Currently writes iqvdataToc and iqvdataSummary into Excel file
    """
    try:
        json_object = json.dumps(data, indent=4)
        json_file_name = os.path.join(settings.PROCESSING_DIR, aidoc_id + ".json")
        with open(json_file_name, "w") as outfile:
            outfile.write(json_object)

        excel_file_name = os.path.join(settings.PROCESSING_DIR, aidoc_id + ".xlsx")
        toc_file_obj = open(json_file_name)
        full_json = json.load(toc_file_obj)
        toc_details = json.loads(json.loads(full_json['iqvdataToc']))
        toc_df = pd.DataFrame(data=toc_details['data'], columns=toc_details['columns'])

        with pd.ExcelWriter(excel_file_name) as writer:
            toc_df.to_excel(writer, index=False, sheet_name="TOC")
            writer.save()
        logger.info(f"Writing data to XLSX file completed : {excel_file_name}")
        return excel_file_name
    except Exception as ex:
        logger.exception(f"Exception occured in writing Data to XLSX file {str(ex)}")
        raise HTTPException(status_code=401, detail=f"Exception occured in writing data to XLSX file {str(ex)}")


async def post_qc_approval_complete_to_mgmt_service(aidoc_id: str, qcApprovedBy: str) -> bool:
    """
    Make a post call to management service to update qc_summary table with updated details
    """
    mgmt_svc_status_code = status.HTTP_404_NOT_FOUND
    try:
        management_api_url = settings.MANAGEMENT_SERVICE_URL + "pd_qc_check_update"
        parameters = {'aidoc_id': aidoc_id, 'qcApprovedBy': qcApprovedBy}
        mgmt_svc_status_code = requests.post(management_api_url, data=parameters)
        logger.debug(f"[{aidoc_id}] QC Approval Complete request sent to Management service")
        
        if mgmt_svc_status_code == status.HTTP_200_OK:
            logger.debug(f"Management service completed with success status: {mgmt_svc_status_code}")
            return True
        else:
            logger.error(f"Management service returned with status: {mgmt_svc_status_code}")
            return False
    except Exception as ex:
        logger.exception(f"Exception occured in posting QC Approval complete to management service {str(ex)}")
        return False
