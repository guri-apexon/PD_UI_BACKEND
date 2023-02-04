from typing import Any, List
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.utilities.config import settings

from app import crud, schemas
from app.api import deps
# from app.models.pd_user_protocols import PD_User_Protocols
from app.models.pd_protocol_alert import ProtocolAlert
from app.schemas.pd_user_alert import UserAlertInput, UserAlert
from datetime import datetime
from app.crud.pd_user_alert import pd_user_alert
from app.api.endpoints import auth

router = APIRouter()

logger = logging.getLogger(settings.PROJECT_NAME)

@router.post("/")
def update_notification_read(notification_read_in: schemas.NotificationRead, db: Session = Depends(deps.get_db), _: str = Depends(auth.validate_user_token)) -> Any:
    """
    Update protocol alerts read notification generated for user for the protocol which the user "follows"
    """
    logger.debug("Alert read notification started.")
    response = pd_user_alert.update_notification_read_status(notification_read_in, db)
    return response
