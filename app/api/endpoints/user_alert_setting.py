from typing import Any
import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utilities.config import settings

from app import schemas
from app.api import deps
from app.crud.pd_user_alert_setting import user_alert_setting
from app.api.endpoints import auth

router = APIRouter()

logger = logging.getLogger(settings.PROJECT_NAME)


@router.get("/")
async def get_user_alert_setting(
        db: Session = Depends(deps.get_db),
        user_id: str = "",
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Collect user alerts setting options, config by user
    """
    logger.debug("To get user alert global setting options")
    user_alert_options = user_alert_setting.get_by_user_id(db, user_id=user_id)
    return user_alert_options if user_alert_options else False


@router.post("/update_setting/")
async def update_user_alert_setting(
        *,
        db: Session = Depends(deps.get_db),
        obj_in: schemas.UserAlertSettingData,
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Update user alert setting options, config by user
    """
    logger.debug("To update user alert global setting options")
    user_alert_data = user_alert_setting.update_user_alert_setting(db,
                                                                   obj_in=obj_in)
    return user_alert_data
