from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.api.endpoints import auth

router = APIRouter()


@router.post("/new_user", response_model=schemas.LoginBaseInDBBase)
def adding_new_user(*, db: Session = Depends(deps.get_db), new_user: schemas.UserCreate,
                    _: str = Depends(auth.validate_user_token)) -> Any:
    # The Minimum Values Are Set For Every Column Name Kindly Checkout Schemas of pd_user
    if new_user.username == "" or new_user.first_name == "" or new_user.last_name == "" or \
            new_user.email == "" or new_user.country == "" or new_user.user_type == "":
        raise HTTPException(status_code=422,
                            detail="Unable To Add New User In The DB Please Provide All The Details Above.")

    login_exist = crud.login.get_by_username(db, new_user.username)
    if login_exist:
        user_exist = crud.user.get_by_username(db, new_user.username)
        if user_exist:
            update_status = crud.login.update_status(db, obj_in=login_exist)
            if update_status:
                return user_exist
            else:
                raise HTTPException(status_code=400, detail=f"Login status updating failed Details:{update_status}")
        else:
            user_create = crud.user.create(db, obj_in=new_user, login_id=login_exist.id)
            return user_create
    else:
        user_added = crud.login.add_user(db, obj_in=new_user)
        if user_added:
            user_create = crud.user.create(db, obj_in=new_user, login_id=user_added.id)
            return user_create
