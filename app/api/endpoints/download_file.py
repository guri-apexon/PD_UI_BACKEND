import logging
import os

from app.api.endpoints import auth
from app.utilities.config import settings
from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse, Response

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)

@router.get("/")
async def download_file(filePath: str = "filePath", _: str = Depends(auth.validate_user_token)):
    '''
    Sends valid file's contents
    '''
    try:
        return stream_file(filePath)
    except Exception as exc:
        logger.error(f"Exception received while downloading file[{filePath}] : [{str(exc)}]")
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=f"{str(exc)}")

def stream_file(file_path):
    """
    Streams file contents with appropriate headers
    """
    download_filename = os.path.basename(file_path)
    if not os.path.exists(file_path):
        logger.error(f"Download file is not accessible at: [{file_path}]")
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=f"Download file is not accessible")

    return FileResponse(file_path, filename=download_filename)
