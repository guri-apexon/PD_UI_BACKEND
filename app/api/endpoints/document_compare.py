import logging
import os

from app import config
from app.api import deps
from app import crud, schemas, config
from app.api.endpoints import auth
from app.api.endpoints.download_file import stream_file
from app.crud.pd_document_compare import pd_document_compare
from app.utilities.config import settings
from fastapi import APIRouter, Depends, status, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.utilities.redact import redactor

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)

@router.get("/")
async def get_compare_doc(
        db: Session = Depends(deps.get_db),
        id1: str = Query(..., description = "id1"),
        id2: str = Query(..., description = "id2"),
        userId: str = None,
        protocol: str = None,
        file_type: str = Query(..., description = "file extension"),
        action_type: str = config.COMPARED_DOC_ACTION_TYPE,
        _: str = Depends(auth.validate_user_token)
):
    """
    1. Streams compare result file
    2. If the number of compare changes is not positive, returns HTTP_204_NO_CONTENT status code 
    """
    try:
        download_allow_flg, redact_profile_name = redactor.check_allow_download(current_db=db, user_id = userId, protocol=protocol, action_type=action_type)
        if not download_allow_flg:
            logger.debug(f"Denied {action_type} for {userId}/{protocol}; redact_profile_name: {redact_profile_name}")
            return Response(status_code=status.HTTP_403_FORBIDDEN, content=f"Denied {action_type} for {userId}/{protocol}")

        document_process = pd_document_compare.get_compare_path(db, id1, id2, redact_profile_name)
        
        if document_process is None or document_process.numChangesTotal is None:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="Compare result is not available for the selected documents")

        num_compare_changes = document_process.numChangesTotal
        if num_compare_changes <= 0:
            logger.debug(f"No compare changes for id1[{id1}] and id2[{id2}]: [numChangesTotal={num_compare_changes}]")
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        document_compare_path = (settings.DFS_UPLOAD_FOLDER + '/compare/' + document_process.compareId)
        file_suffix = 'compare_detail'+file_type
        file_name = None
        if os.path.isdir(document_compare_path):
            for file in os.listdir(document_compare_path):
                if file.endswith(file_suffix):
                    file_name = file
                    break
            if not file_name:
                logger.error(f"Compare result is not available in {file_type} format")
                return Response(status_code=status.HTTP_404_NOT_FOUND,
                                content=f"Compare result is not available in {file_type} format")
            else:
                file_path = (document_compare_path + '/' + file_name)
                return stream_file(file_path)
        else:
            return Response(status_code=status.HTTP_404_NOT_FOUND,
                            content="Compare result is not available for the selected documents")

    except Exception as exc:
        logger.error(f"Exception received for id1[{id1}] and id2[{id2}]: {str(exc)}")
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=f"{str(exc)}")
