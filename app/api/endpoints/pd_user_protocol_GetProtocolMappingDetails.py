from typing import Any, List
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utilities.config import settings

from app import crud, schemas
from app.api import deps
from app.models.pd_user_protocols import PD_User_Protocols
from app.api.endpoints import auth

router = APIRouter()

logger = logging.getLogger(settings.PROJECT_NAME)

@router.get("/read_user_protocols_by_userId_or_protocol")
def read_user_protocol(*,
                       db: Session = Depends(deps.get_db),
                       userId: str = None,
                       protocol: str = None ,_: str = Depends(auth.validate_user_token)
                       ) -> Any:
    if userId or protocol:
        user_protocols = crud.pd_user_protocols.get_details_by_userId_protocol(db, userId, protocol)
        if user_protocols:
            return user_protocols
        else:
            raise HTTPException(status_code=422, detail="No record found for the given userId or Protocol")
    else:
        raise HTTPException(status_code=422, detail="No record found for the given userId or Protocol")
