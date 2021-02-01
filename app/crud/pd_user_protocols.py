from typing import Any, Dict, Optional, Union
from datetime import datetime
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pd_user_protocols import PD_User_Protocols
from app.schemas.pd_user_protocols import UserProtocolCreate, UserProtocolUpdate, UserProtocolAdd


class CRUDUserProtocols(CRUDBase[PD_User_Protocols, UserProtocolCreate, UserProtocolUpdate]):
    def get_by_id(self, db: Session, *, id: Any, userId: Any) -> Optional[PD_User_Protocols]:
        return db.query(PD_User_Protocols).filter(PD_User_Protocols.id == id).filter(
            PD_User_Protocols.userId == userId).first()

    def create(self, db: Session, *, obj_in: UserProtocolCreate) -> PD_User_Protocols:
        db_obj = PD_User_Protocols(isActive=obj_in.isActive,
                                   id=obj_in.id,
                                   userId=obj_in.userId,
                                   protocol=obj_in.protocol,
                                   follow=obj_in.follow,
                                   userRole=obj_in.userRole,
                                   userCreated=obj_in.userCreated,
                                   timeCreated=obj_in.timeCreated,
                                   userUpdated=obj_in.userUpdated,
                                   lastUpdated=obj_in.lastUpdated, )
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as ex:
            db.rollback()
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

    def add_protocol(self, db: Session, *, obj_in: UserProtocolAdd) -> PD_User_Protocols:
        # Check for the duplicate entry with the given userId and Protocol
        user_protocol = pd_user_protocols.get_by_userid_protocol(db, obj_in.userId, obj_in.protocol)
        if user_protocol:
            raise HTTPException(
                status_code=404,
                detail=f"Already record exists with the given {obj_in.userId} and {obj_in.protocol} with userRole {obj_in.userRole} ",
            )
        db_obj = PD_User_Protocols(isActive=True,
                                   userId=obj_in.userId,
                                   protocol=obj_in.protocol,
                                   follow=False,
                                   userRole=obj_in.userRole,
                                   projectId=obj_in.projectId,
                                   userCreated=obj_in.userCreated,
                                   timeCreated=datetime.now(),
                                   userUpdated=obj_in.userUpdated,
                                   lastUpdated=datetime.now(), )
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as ex:
            db.rollback()
        return db_obj

    def get_by_userid_protocol(self, db: Session, userid: Any, protocol: Any) -> PD_User_Protocols:
        """Deletes record in DB table"""
        return db.query(self.model).filter(PD_User_Protocols.userId == userid).filter(
            PD_User_Protocols.protocol == protocol).first()


pd_user_protocols = CRUDUserProtocols(PD_User_Protocols)
