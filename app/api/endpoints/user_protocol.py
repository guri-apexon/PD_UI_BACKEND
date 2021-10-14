from typing import Any
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utilities.config import settings

from app import crud, schemas
from app.api import deps
from app.api.endpoints import auth

router = APIRouter()

logger = logging.getLogger(settings.PROJECT_NAME)


@router.post("/", response_model=schemas.UserProtocol)
def add_user_protocol_one_to_one(
        *,
        db: Session = Depends(deps.get_db),
        user_protocol_in: schemas.UserProtocolAdd,
        _: str = Depends(auth.validate_user_token),
) -> Any:
    """
    Add User Protocol One To One.
    """
    if user_protocol_in.userId == "" or user_protocol_in.protocol == "" or user_protocol_in.follow == "" or user_protocol_in.userRole == "":
        raise HTTPException(status_code=403, detail=f"Can't Add with null values userId:{user_protocol_in.userId},"
                                                    f" protocol:{user_protocol_in.protocol},"
                                                    f" follow:{user_protocol_in.follow} & userRole:{user_protocol_in.userRole}")
    logger.info("add_user_protocol_one_to_one POST method called")
    user_protocol = crud.pd_user_protocols.add_protocol(db, obj_in=user_protocol_in)
    if not user_protocol:
        raise HTTPException(
            status_code=404,
            detail="Exception occurred. Unable to Add User Protocol",
        )
    return user_protocol


@router.delete("/", response_model=schemas.UserProtocol)
def delete_user_protocol(
        *,
        db: Session = Depends(deps.get_db),
        userId: str = "id",
        protocol: str = "Protocol",
        _: str = Depends(auth.validate_user_token),
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


@router.get("/is_primary_user")
def is_user_primary(
        *,
        db: Session = Depends(deps.get_db),
        _: str = Depends(auth.validate_user_token),
        userId: str = "id",
        protocol: str = "Protocol",
) -> Any:
    """
    Check whether the given user with protocol is primary or not
    """
    user_protocol = crud.pd_user_protocols.get_by_userid_protocol(db, userId, protocol)
    # if the user_protocol doesnt exist in DB
    if not user_protocol:
        return 0
    else:
        if user_protocol.userRole == "primary":
            return 1
        else:
            return 0
