import logging
from datetime import datetime
from typing import Any, Dict, Optional, Union

from app import config
from app.crud.base import CRUDBase
from app.utilities.config import settings
from app.models.pd_user_protocols import PD_User_Protocols
from app.schemas.pd_user_protocols import (UserFollowProtocol, UserProtocolAdd,
                                           UserProtocolCreate,
                                           UserProtocolUpdate)
from fastapi import HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session

logger = logging.getLogger(settings.PROJECT_NAME)


class CRUDUserProtocols(CRUDBase[PD_User_Protocols, UserProtocolCreate, UserProtocolUpdate]):
    def get_by_id(self, db: Session, *, id: Any, userId: Any) -> Optional[PD_User_Protocols]:
        return db.query(PD_User_Protocols).filter(PD_User_Protocols.id == id).filter(
            PD_User_Protocols.userId == userId).first()

    def create(self, db: Session, *, obj_in: UserProtocolCreate) -> PD_User_Protocols:
        db_obj = PD_User_Protocols(isActive=obj_in.isActive,
                                   userId=obj_in.userId,
                                   protocol=obj_in.protocol,
                                   follow=obj_in.follow,
                                   userRole=obj_in.userRole,
                                   userCreated=obj_in.userCreated,
                                   timeCreated=obj_in.timeCreated,
                                   userUpdated=obj_in.userUpdated,
                                   lastUpdated=obj_in.lastUpdated)
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as ex:
            db.rollback()
        return db_obj

    def follow_unfollow(self, db: Session, *, obj_in: UserFollowProtocol) -> PD_User_Protocols:
        current_timestamp = datetime.utcnow()
        user_role = config.FOLLOW_DEFAULT_ROLE if obj_in.userRole.lower() not in config.FOLLOW_ALLOWED_ROLES else obj_in.userRole

        # check if record exists for the given userId and Protocol, if exists update else create new record
        user_protocol_obj = db.query(PD_User_Protocols).filter(PD_User_Protocols.userId == obj_in.userId,
            PD_User_Protocols.protocol == obj_in.protocol).first()
        if user_protocol_obj:
            try:
                user_protocol_obj.isActive = True
                user_protocol_obj.follow = obj_in.follow
                user_protocol_obj.userRole = user_role
                user_protocol_obj.lastUpdated = current_timestamp
                db.commit()
                db.refresh(user_protocol_obj)
            except Exception as ex:
                db.rollback()
                raise HTTPException(status_code=401,
                                        detail=f"Exception occurred during follow_unfollow protocol {str(ex)}")
            return user_protocol_obj
        else:
            db_obj = PD_User_Protocols(
                                       isActive = True,
                                       userId = obj_in.userId,
                                       protocol = obj_in.protocol,
                                       follow = obj_in.follow,
                                       userRole = user_role,
                                       timeCreated = current_timestamp,
                                       lastUpdated = current_timestamp
                                    )
            try:
                db.add(db_obj)
                db.commit()
                db.refresh(db_obj)
            except Exception as ex:
                db.rollback()
                raise HTTPException(status_code=401,
                                    detail=f"Exception occurred during follow_unfollow protocol {str(ex)}")
            return db_obj

    def update(self, db: Session, *, db_obj: UserProtocolUpdate,
               obj_in: Union[UserProtocolUpdate, Dict[str, Any]]) -> PD_User_Protocols:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def remove_followed_protocols(self, db: Session, id: Any, userId: Any) -> PD_User_Protocols:
        """Deletes record in DB table"""
        obj = db.query(self.model).filter(PD_User_Protocols.id == id).filter(PD_User_Protocols.userId == userId).first()
        db.delete(obj)
        db.commit()
        return obj

    def follow_protocol(self, db: Session, *, id: Any, userId: Any) -> Optional[PD_User_Protocols]:
        return db.query(PD_User_Protocols).filter(PD_User_Protocols.id == id).filter(
            PD_User_Protocols.userId == userId).first()

    @staticmethod
    def add_protocol(db: Session, *, obj_in: UserProtocolAdd) -> PD_User_Protocols:
        user_protocol = pd_user_protocols.get_by_userid_protocol(db, obj_in.userId, obj_in.protocol)
        if user_protocol:
            raise HTTPException(
                status_code=204,
                detail=f"Already record exists with userId: {obj_in.userId}, "
                       f"protocol: {obj_in.protocol} and userRole: {obj_in.userRole}",
            )

        db_obj = PD_User_Protocols(isActive=True,
                                   userId=obj_in.userId,
                                   protocol=obj_in.protocol,
                                   follow=obj_in.follow,
                                   userRole=obj_in.userRole,
                                   projectId=obj_in.projectId,
                                   userCreated=obj_in.userCreated,
                                   timeCreated=datetime.utcnow(),
                                   userUpdated=obj_in.userUpdated,
                                   lastUpdated=datetime.utcnow(), )
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except exc.SQLAlchemyError as ex:
            db.rollback()
            logger.error(f"SQLAlchemyError raised \n {str(ex)}")
        except Exception as ex:
            db.rollback()
            logger.error(f"Exception received for userID: {obj_in.userId} and "
                         f"protocol: {obj_in.protocol} \n ERROR Details: {str(ex)}")
        return db_obj

    def get_by_userid_protocol(self, db: Session, userid: Any, protocol: Any) -> PD_User_Protocols:
        """Retrieves record from table"""
        return db.query(self.model).filter(PD_User_Protocols.userId == userid).filter(
            PD_User_Protocols.protocol == protocol).filter(PD_User_Protocols.isActive=='1').first()

    def get_details_by_userId_protocol(self, db: Session, userId: Any, protocol: Any) -> PD_User_Protocols:
        try:
            if userId and not protocol:
                result = db.query(PD_User_Protocols.userId, PD_User_Protocols.protocol,
                                  PD_User_Protocols.isActive, PD_User_Protocols.follow,
                                  PD_User_Protocols.userRole, PD_User_Protocols.timeCreated,
                                  PD_User_Protocols.lastUpdated).filter(PD_User_Protocols.userId == userId,
                                                                        PD_User_Protocols.isActive == '1').all()

            elif not userId and protocol:
                result = db.query(PD_User_Protocols.userId, PD_User_Protocols.protocol,
                                  PD_User_Protocols.isActive, PD_User_Protocols.follow,
                                  PD_User_Protocols.userRole, PD_User_Protocols.timeCreated,
                                  PD_User_Protocols.lastUpdated).filter(PD_User_Protocols.protocol == protocol,
                                                                        PD_User_Protocols.isActive == '1').all()
            elif userId and protocol:
                result = db.query(PD_User_Protocols.userId, PD_User_Protocols.protocol,
                                  PD_User_Protocols.isActive, PD_User_Protocols.follow,
                                  PD_User_Protocols.userRole, PD_User_Protocols.timeCreated,
                                  PD_User_Protocols.lastUpdated).filter(PD_User_Protocols.userId == userId,
                                                                        PD_User_Protocols.protocol == protocol,
                                                                        PD_User_Protocols.isActive == '1').all()
            return result
        except Exception as ex:
            return ex

pd_user_protocols = CRUDUserProtocols(PD_User_Protocols)
