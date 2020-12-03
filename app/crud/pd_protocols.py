from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pd_protocols import PD_Protocols
from app.schemas.pd_protocols import ProtocolCreate, ProtocolUpdate


class CRUDProtocols(CRUDBase[PD_Protocols, ProtocolCreate, ProtocolUpdate]):
    def get_by_id(self, db: Session, *, protocol_id: int) -> Optional[PD_Protocols]:
        return db.query(PD_Protocols).filter(PD_Protocols.id == protocol_id).first()

    def create(self, db: Session, *, obj_in: ProtocolCreate) -> PD_Protocols:
        db_obj = PD_Protocols(protocol_number=obj_in.protocol_number,
                                            protocol_title=obj_in.protocol_title,
                                            project_code=obj_in.project_code,
                                            phase=obj_in.phase,
                                            indication=obj_in.indication,
                                            protocol_status=obj_in.protocol_status,
                                            protocol_version=obj_in.protocol_version,
                                            protocol_sponsor=obj_in.protocol_sponsor,
                                            is_active=obj_in.is_active,
                                            created_by=obj_in.created_by,
                                            created_on=obj_in.created_on,
                                            modified_by=obj_in.modified_by,
                                            modified_on=obj_in.modified_on, )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
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
