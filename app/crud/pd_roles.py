from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.pd_roles import Roles
from app.schemas.pd_roles import RolesBaseInDBBase, RolesUpdate, RolesCreate
from app import schemas
class CRUDRoles(CRUDBase[Roles, RolesBaseInDBBase, RolesCreate]):
    def get_all_roles(self, db:Session) -> Roles:
        return db.query(Roles).all()

    def get_by_roleName(self, db:Session, roleName:str) -> Roles:
        return db.query(Roles).filter(Roles.roleName == roleName).first()


    def create(self, db: Session, *, obj_in: schemas.RolesCreate) -> Roles:
        try:
            db_obj = Roles(roleName=obj_in.roleName, roleDescription=obj_in.roleDescription)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as ex:
            db.rollback()
            return ex


roles = CRUDRoles(Roles)
