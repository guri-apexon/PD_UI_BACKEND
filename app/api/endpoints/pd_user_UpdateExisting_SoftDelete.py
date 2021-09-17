from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app import crud, schemas
from app.api import deps
from app.api.endpoints import auth

router = APIRouter()

#For Updating the existing user details
@router.put("/update_existing", response_model=bool)
def update_existing(*, db: Session = Depends(deps.get_db), update_user:schemas.UserUpdate, _: str = Depends(auth.validate_user_token)):
   user_username_exist = crud.user.get_by_username(db, update_user.username)
   if user_username_exist:
       try:
           if update_user.username is not None:
               updated_user = crud.user.update(db, obj_in=update_user)
               return updated_user
           else:
               return False
       except Exception as ex:
           raise HTTPException(status_code=403, detail=f"Exception occurred while updating is {str(ex)}")
   else:
       raise HTTPException(status_code=404, detail="No user found with given username.")

#For Soft Deleting(changing 1 to 0 of internal_user column in Login Table)
@router.put("/delete_user", response_model=bool)
def deleting_user(*, db: Session = Depends(deps.get_db), user_status: schemas.User_Soft_Delete, _: str = Depends(auth.validate_user_token)):
    login_username_exist = crud.login.get_by_username(db, user_status.username)
    if login_username_exist:
        try:
            if user_status.active_user is not None and type(user_status.active_user) == bool and user_status.active_user == False:
                status = crud.login.soft_delete(db, obj_in=user_status)
                return status
            else:
                return False
        except Exception as ex:
            raise HTTPException(status_code=403, detail=f"Exception occurred while deleting(soft delete) is {str(ex)}")
    else:
        raise HTTPException(status_code=404, detail="No user found with given username.")
