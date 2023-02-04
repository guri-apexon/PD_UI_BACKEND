import logging
import os

from app import config
from app.api import deps
from app.api.endpoints import auth
from app.utilities.config import settings
from app.utilities.redact import redactor
from fastapi import APIRouter, Depends, status
from fastapi.responses import FileResponse, Response
from sqlalchemy.orm import Session

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)

@router.get("/")
async def download_file(filePath: str = "filePath", userId: str = None, protocol: str = None, action_type: str = config.SRC_DOC_ACTION_TYPE,
                            db: Session = Depends(deps.get_db),_: str = Depends(auth.validate_user_token)):
    '''
    Sends valid file's contents
    '''
    try:
        if userId == 'qc':
            download_allow_flg = True
        else:    
            download_allow_flg, redact_profile_name = redactor.check_allow_download(current_db=db, user_id = userId, protocol=protocol, action_type=action_type)

        if download_allow_flg:
            return stream_file(filePath)
        else:
            logger.debug(f"Denied {action_type} for {userId}/{protocol}, redact_profile_name: {redact_profile_name}")
            return Response(status_code=status.HTTP_403_FORBIDDEN, content=f"Denied {action_type} for {userId}/{protocol}")
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
