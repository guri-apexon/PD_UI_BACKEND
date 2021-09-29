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

@router.put("/delete_userprotocol")
def remove_user_protocol_mapping(*, db:Session= Depends(deps.get_db), user_protocol: schemas.UserProtocolSoftDelete, _: str = Depends(auth.validate_user_token)):
    if user_protocol.isActive is not None and type(user_protocol.isActive) == bool and user_protocol.isActive == False:
        status = crud.pd_user_protocols.soft_delete(db, obj_in=user_protocol)
        print(status)
        if status is True:
            return {'status_code': 200, 'detail': "Record deleted succesfully"}
        else:
            raise HTTPException(status_code=403, detail="Data Not Found for given userId or protocol")
    else:
        raise HTTPException(status_code=403, detail="Check whether the input given for isActive & of boolean or not.")