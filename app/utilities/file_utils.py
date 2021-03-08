import json
import os
import shutil
from pathlib import Path

import pandas as pd
from fastapi import UploadFile, HTTPException
from starlette import status

from app.utilities.config import settings


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


def validate_qc_protocol_file(doc_id: str, file_content_type: str,
                              ):
    """
    Validates the xml file type content before processing
    """
    if not (file_content_type in ['application/vnd.ms-excel',
                                  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                  'application/json']):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Invalid file uploaded received - only json or excel files are accepted",
        )


def write_data_to_json(aidoc_id: str, data: str):
    json_object = json.dumps(data, indent=4)
    json_file_name = os.path.join(settings.PROCESSING_DIR, aidoc_id + ".json")
    with open(json_file_name, "w") as outfile:
        outfile.write(json_object)
    return json_file_name


def write_data_to_xlsx(aidoc_id: str, data: str):
    json_object = json.dumps(data, indent=4)
    json_file_name = os.path.join(settings.PROCESSING_DIR, aidoc_id + ".json")
    with open(json_file_name, "w") as outfile:
        outfile.write(json_object)
    excel_file_name = os.path.join(settings.PROCESSING_DIR, aidoc_id + ".xlsx")
    try:
        json_file_obj = open(json_file_name)
        json_data = json.load(json_file_obj)
        file_df = pd.DataFrame(data=list(json_data.items()))
        file_df_transpose = file_df.T
        file_df_transpose.to_excel(excel_file_name, index=False, engine='xlsxwriter')
    except Exception as ex:
        raise HTTPException(status_code=403, detail=f"Exception Occurred : {str(ex)}")
    return excel_file_name
