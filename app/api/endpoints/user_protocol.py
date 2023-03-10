from typing import Any
import logging

from fastapi import APIRouter, UploadFile, Depends, HTTPException, File
from sqlalchemy.orm import Session
from starlette import status
from app.utilities.config import settings

from app import crud, schemas
from app.api import deps
from app.api.endpoints import auth
from app.utilities.file_utils import save_bulkmap_file

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
    if user_protocol_in.userId == "" or user_protocol_in.protocol == "" or user_protocol_in.follow == "" or user_protocol_in.userRole == "" or user_protocol_in.accessReason == "":
        raise HTTPException(status_code=403, detail=f"Can't Add with null values userId:{user_protocol_in.userId},"
                                                    f" protocol:{user_protocol_in.protocol},"
                                                    f" follow:{user_protocol_in.follow}, & userRole:{user_protocol_in.userRole} & accessReason:{user_protocol_in.accessReason}")
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


@router.post("/user_protocol_many")
def add_user_protocol_many_to_many(*, user_protocol_xls_file: UploadFile = File(..., description="Upload User_Protocol Excel File(.xlsx)"),
                                   user_updated: str,
                                   access_reason: str,
                                   db: Session = Depends(deps.get_db),
                              _: str = Depends(auth.validate_user_token)) -> Any:
    try:
        user_protocol_path = save_bulkmap_file(user_protocol_xls_file)
        user_protocol_updation_status = crud.pd_user_protocols.excel_data_to_db(
            db, user_protocol_path, user_updated, access_reason)
        if user_protocol_updation_status==False:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                                detail="Invalid File Type Received, Please Provide Excel(.xlsx) file only")
        else:
            return user_protocol_updation_status

    except Exception as ex:
        logger.exception(f'pd-ui-backend: Exception occured in qc_protocol_upload {str(ex)}')
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail="Invalid file received, please provide excel file(.xlsx format) or Excel file may not contain data " + str(ex))


@router.put("/delete_userprotocol")
def remove_user_protocol_mapping(*, db:Session= Depends(deps.get_db), user_protocol: schemas.UserProtocolSoftDelete, _: str = Depends(auth.validate_user_token)) -> Any:
    if user_protocol.userId and user_protocol.userId.strip() and user_protocol.protocol and user_protocol.protocol.strip() and user_protocol.isActive is not None:
        if type(user_protocol.isActive) == bool and user_protocol.isActive == False:
            status = crud.pd_user_protocols.soft_delete(db, obj_in=user_protocol)
            if status is True:
                return {'status_code': 200, 'detail': "Record deleted successfully"}
            else:
                raise HTTPException(status_code=403, detail="Data Not Found for given userId or protocol")
        else:
            raise HTTPException(status_code=403, detail="Check whether you have given all inputs correctly & false for isActive(Boolean type).")
    else:
        raise HTTPException(status_code=403, detail="Unable To Delete Please Provide All The Details Above And false for isActive(boolean type).")


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