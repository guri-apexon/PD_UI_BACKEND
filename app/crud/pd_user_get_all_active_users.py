from typing import Any, Dict, Optional, Union, List

from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.pd_user import User
from app.schemas.pd_user import UserUpdate, UserCreate, UserBaseInDBBase
from app.models.pd_login import Login


class CRUDUserSearch(CRUDBase[User, UserUpdate, UserCreate]):
    def get_all_user(self,db:Session) -> User:
           return db.query(User.username, User.first_name, User.last_name, User.email, User.country, User.date_of_registration, User.user_type).join(Login, and_(Login.id == User.login_id, Login.internal_user == '1')).all()

user = CRUDUserSearch(User)