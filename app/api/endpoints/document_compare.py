import logging


from app.api import deps
from app import crud, schemas, config
from app.api.endpoints import auth
from app.api.endpoints.download_file import stream_file
from app.crud.pd_document_compare import pd_document_compare
from app.utilities.config import settings
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)

@router.get("/")
async def get_compare_doc(
        db: Session = Depends(deps.get_db),
        id1: str = "id1",
        id2: str = "id2",
        user_id: str = "userId",
        protocol_number: str = "protocolNumber",
        _: str = Depends(auth.validate_user_token)
):
    """
    1. Streams compare result file
    2. If the number of compare changes is not positive, returns HTTP_204_NO_CONTENT status code 
    """
    
    try:
        resource = crud.pd_user_protocols.get_user_role(db, user_id, protocol_number)
        if resource is None:
            logger.exception(f'No user available for userId:{user_id} and protocol:{protocol_number} in pd_user_protocols Table.')
            raise Response(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user available for userId {user_id} and protocol {protocol_number}.")
        else:
            user_role = resource.userRole.lower()
            redact_profile = config.USERROLE_REDACTPROFILE_MAP[user_role] 

        document_process = pd_document_compare.get_compare_path(db, id1, id2, redact_profile)
        
        if document_process is None or document_process.numChangesTotal is None:
            return Response(status_code=status.HTTP_404_NOT_FOUND, content="Compare result is not available for the selected documents")

        num_compare_changes = document_process.numChangesTotal
        if num_compare_changes <= 0:
            logger.debug(f"No compare changes for id1[{id1}] and id2[{id2}]: [numChangesTotal={num_compare_changes}]")
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        return stream_file(document_process.compareCSVPath)

    except Exception as exc:
        logger.error(f"Exception received for id1[{id1}] and id2[{id2}]: {str(exc)}")
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=f"{str(exc)}")
