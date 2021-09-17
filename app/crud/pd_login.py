from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from datetime import datetime
from app import schemas
from app.models.pd_login import Login
from app.schemas.pd_login import LoginBaseInDBBase, User_Soft_Delete
from app import schemas
from app.models.pd_user import User
from sqlalchemy import and_

class CRUDLoginUser(CRUDBase[Login, LoginBaseInDBBase, User_Soft_Delete]):
    def get_by_username(self, db:Session, username:str) -> Login:
        return db.query(Login).filter(User.username == username).first()

    def soft_delete(self, db: Session, obj_in:schemas.User_Soft_Delete) -> Login:
        try:
            result = db.query(Login).filter(and_(Login.username == obj_in.username, Login.active_user == True)).first()
            if result:
                result_user = db.query(User).filter(User.username == obj_in.username).first()
                if result_user:
                    result.active_user = obj_in.active_user
                    result.lastUpdated = datetime.utcnow()
                    result_user.lastUpdated = datetime.utcnow()
                    db.add(result_user)
                    db.add(result)
                    db.commit()
                    return True
                else:
                    return False
            else:
                return False
        except Exception as ex:
            db.rollback()
            return ex

login = CRUDLoginUser(Login)