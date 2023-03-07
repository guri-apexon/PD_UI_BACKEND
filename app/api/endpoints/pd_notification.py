import logging
from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.api.endpoints import auth
from app import crud
from app.utilities.config import settings

router = APIRouter()
logger = logging.getLogger(settings.LOGGER_NAME)

@router.get("/")
async def get_notifications(
    user_id: str,
    db: Session = Depends(deps.get_db),
    # _ : str = Depends(auth.validate_user_token)
) -> Any:
    """
    Get All notification
    :param user_id: user id to fetch notification
    :param db: database instance
    """
    
    all_notifications = crud.get_notifications_from_db(db, user_id)
    return all_notifications



@router.get("/update")
async def update_notification_read_record(
    aidocId: str,
    id: str,
    protocol: str,
    action: str,
    db: Session = Depends(deps.get_db),
    # _ : str = Depends(auth.validate_user_token)
) -> Any:
    """
    Update notification record in ProtocolAlert table 
    :param aidocId: document id
    :param id: id of protocol alert table
    :param protocol: protocol number
    :param action: action is notification is read or delete
                if read update readflag if delete update isactive flag in protocol alert table 
    """

    notification_status = crud.read_or_delete_notification(db, aidocId, id, protocol, action)
    return notification_status

