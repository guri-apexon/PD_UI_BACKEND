from typing import Any, Dict, Optional, Union, List

from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.pd_user import User
from app.schemas.pd_user import UserUpdate, UserCreate, UserBaseInDBBase
from app.models.pd_login import Login


class CRUDUserSearch(CRUDBase[User, UserUpdate, UserCreate]):
    def get_all_user(self, db: Session, userId: str = None) -> User:
        if userId is not "":
            search = "%{}%".format(userId)
            protocolmetadata_data = db.query(User.username, User.first_name, User.last_name).filter(
                User.username.like(search)).first()
            return protocolmetadata_data
        else:
            return db.query(User.username, User.first_name, User.last_name, User.email, User.country,
                            User.date_of_registration, User.user_type).join(Login, and_(Login.id == User.login_id,
                                                                                        Login.active_user == '1')).all()

    def get_by_username(self, db:Session, username:str) -> User:
        return db.query(User).filter(User.username == username).first()

    def update(self, db: Session, obj_in: UserUpdate, ) -> User:
        user = db.query(User).filter(User.username == obj_in.username).first()

        if not user:
            return False
        try:
            user.first_name = obj_in.first_name if obj_in.first_name else user.first_name
            user.last_name = obj_in.last_name if obj_in.last_name else user.last_name
            user.email = obj_in.email if obj_in.email else user.email
            user.country = obj_in.country if obj_in.country else user.country
            user.user_type = obj_in.user_type if obj_in.user_type else user.user_type
            db.add(user)
            db.commit()
            return True
        except Exception as ex:
            db.rollback()
            return ex


user = CRUDUserSearch(User)