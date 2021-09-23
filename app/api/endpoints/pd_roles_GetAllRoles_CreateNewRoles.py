from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.api.endpoints import auth

router = APIRouter()

@router.get("/get_all_roles")
def get_all_roles(*, db: Session = Depends(deps.get_db),
                  _: str = Depends(auth.validate_user_token)) -> Any:
    all_roles = crud.roles.get_all_roles(db)
    return all_roles

@router.post("/new_role",response_model=schemas.RolesBaseInDBBase)
def create_new_roles(*, db:Session = Depends(deps.get_db), new_role: schemas.RolesCreate,
                     _: str = Depends(auth.validate_user_token)):
    if new_role.roleName == "" or new_role.roleDescription == "":
        raise HTTPException(status_code= 422, detail="Unable To Add New Role Details Please Fill All The Details Above.")

    role = crud.roles.get_by_roleName(db, new_role.roleName)
    if role:
        raise HTTPException(status_code=422, detail="Role Details Already Exist With The Given Above Role Name Along With Some Description")
    else:
        role_create = crud.roles.create(db, obj_in=new_role)
        return role_create
