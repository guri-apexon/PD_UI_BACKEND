from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.pd_user import User
from app.schemas.pd_user import UserUpdate, UserCreate, UserBaseInDBBase
from app.models.pd_login import Login
from app import config


class CRUDUserSearch(CRUDBase[User, UserUpdate, UserCreate]):
    def get_all_user(self, db: Session, userId: str = None) -> User:
        if userId and userId != "":
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
            user.lastUpdated = datetime.utcnow()
            user.reason_for_change = obj_in.reason_for_change if obj_in.reason_for_change else user.reason_for_change
            db.add(user)
            db.commit()
            return True
        except Exception as ex:
            db.rollback()
            return ex

    def create(self, db: Session, *, obj_in: UserCreate, login_id) -> User:
        try:
            db_obj = User(
                            first_name=obj_in.first_name,
                            last_name=obj_in.last_name,
                            country=obj_in.country,
                            email=obj_in.email,
                            username=obj_in.username,
                            login_id=login_id,
                            user_type=obj_in.user_type,
                            reason_for_change=obj_in.reason_for_change)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except Exception as ex:
            db.rollback()
            return ex

    def get_by_username_list(self, db:Session, user_ids:list):
        user_ids = [config.REGEX_EMP_ID_ALPHA_REPLACE.sub('', user_id) for user_id in user_ids]
        if 'user_details' not in self.__dict__ or self.user_details == None or any(
                (False for user_id in user_ids if user_id not in self.user_details)):
            self.update_user_details(db)

        user_details_ret = {user_id:self.user_details.get(user_id, None) for user_id in user_ids}
        user_details_ret = {user_id:user_detail for user_id, user_detail in user_details_ret.items() if user_detail}

        return user_details_ret

    def update_user_details(self, db:Session):
        self.user_details = self.get_all_user(db)
        self.user_details = {config.REGEX_EMP_ID_ALPHA_REPLACE.sub('', detail.username): detail for detail in self.user_details}

user = CRUDUserSearch(User)