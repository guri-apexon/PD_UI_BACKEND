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

@router.get("/", response_model=List[UserAlert])
def get_user_alert(
        *,
        db: Session = Depends(deps.get_db),
        userId: str,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Collect protocol alerts generated for this user for the protocols which the user "follows"
    """
    logger.debug("User alerts extraction starts")
    user_alerts = pd_user_alert.get_by_userid(db, user_id = userId)
    return user_alerts
