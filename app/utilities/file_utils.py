import shutil
from pathlib import Path

from app.utilities.config import settings
from fastapi import UploadFile, HTTPException
from starlette import status


def save_request_file(_id, upload_file: UploadFile):
    """
    Saves the request files in the processing folder
    """
    req_dir = Path(settings.PROCESSING_DIR, 'temp')
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


def validate_xml_file(doc_id: str, file_content_type: str,
                      ):
    """
    Validates the xml file type content before processing
    """
    # if not (file_content_type in ['text/xml', "application/xml"]):
    if not (file_content_type in ['application/vnd.ms-excel',
                                  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet']):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Invalid Excel file received",
            headers={"doc-id": doc_id},
        )
