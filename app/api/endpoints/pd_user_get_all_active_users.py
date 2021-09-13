from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app import crud, schemas
from app.api import deps
from app.api.endpoints import auth

router = APIRouter()

#For getting All Active Users
@router.get("/read_all_users")
def get_all_users(*, db: Session = Depends(deps.get_db), _: str = Depends(auth.validate_user_token)) -> Any:

   user_search = crud.user.get_all_user(db)
   return user_search