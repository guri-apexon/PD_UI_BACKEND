from typing import Any, List
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utilities.config import settings

from app import crud, schemas
from app.api import deps
from app.models.pd_user_protocols import PD_User_Protocols

router = APIRouter()

logger = logging.getLogger(settings.PROJECT_NAME)

@router.post("/", response_model=schemas.UserProtocol)
def add_user_protocol(
        *,
        db: Session = Depends(deps.get_db),
        user_protocol_in: schemas.UserProtocolAdd,
) -> Any:
    """
    push follow protocol data.
    """
    logger.info("add_user_protocol POST method called")
    user_protocol = crud.pd_user_protocols.add_protocol(db, obj_in=user_protocol_in)
    if not user_protocol:
        raise HTTPException(
            status_code=404,
            detail="Exception occured. Unable to Add User Protocol",
        )
    return user_protocol


@router.delete("/", response_model=schemas.UserProtocol)
def delete_user_protocol(
        *,
        db: Session = Depends(deps.get_db),
        userId: str = "id",
        protocol: str = "Protocol",
) -> Any:
    """
    Soft Delete a User Protocol - updates is_Active to false
    """
    logger.info("add_user_protocol DELETE method called")
    user_protocol = crud.pd_user_protocols.get_by_userid_protocol(db, userId, protocol)
    # if the user_protocol doesnt exist in DB
    if not user_protocol:
        raise HTTPException(
            status_code=404,
            detail="No Record exists with the given userId and Protocol.",
        )
    user_protocol.isActive = False
    try:
        db.commit()
        db.refresh(user_protocol)
    except Exception as ex:
        db.rollback()
    return user_protocol
