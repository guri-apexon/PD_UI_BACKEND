from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pd_protocols import PD_Protocols
from app.schemas.pd_protocols import ProtocolCreate, ProtocolUpdate


class CRUDProtocols(CRUDBase[PD_Protocols, ProtocolCreate, ProtocolUpdate]):
    def get_by_id(self, db: Session, *, protocolId: int) -> Optional[PD_Protocols]:
        return db.query(PD_Protocols).filter(PD_Protocols.id == protocolId).first()

    def create(self, db: Session, *, obj_in: ProtocolCreate) -> PD_Protocols:
        db_obj = PD_Protocols(protocol=obj_in.protocol,
                                            protocolTitle=obj_in.protocolTitle,
                                            projectCode=obj_in.projectCode,
                                            phase=obj_in.phase,
                                            indication=obj_in.indication,
                                            protocolStatus=obj_in.protocolStatus,
                                            protocolVersion=obj_in.protocolVersion,
                                            protocolSponsor=obj_in.protocolSponsor,
                                            isActive=obj_in.isActive,
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

    def update(
            self, db: Session, *, db_obj: PD_Protocols, obj_in: Union[ProtocolUpdate, Dict[str, Any]]
    ) -> PD_Protocols:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


pd_protocols = CRUDProtocols(PD_Protocols)
