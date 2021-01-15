from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pd_protocol_data import PD_Protocol_Data
from app.schemas.pd_protocol_data import ProtocolDataCreate, ProtocolDataUpdate, ProtocolData


class CRUDProtocolData(CRUDBase[PD_Protocol_Data, ProtocolDataCreate, ProtocolDataUpdate]):
    def get_by_id(self, db: Session, *, id: Any) -> Optional[PD_Protocol_Data]:
        return db.query(PD_Protocol_Data).filter(PD_Protocol_Data.id == id).first()

    def create(self, db: Session, *, obj_in: ProtocolDataCreate) -> PD_Protocol_Data:
        db_obj = PD_Protocol_Data(id=obj_in.id,
                                    userId=obj_in.userId,
                                    fileName=obj_in.fileName,
                                    documentFilePath=obj_in.documentFilePath,
                                    iqvdataToc=obj_in.iqvdataToc,
                                    iqvdataSoa=obj_in.iqvdataSoa,
                                    iqvdataSoaStd=obj_in.iqvdataSoaStd, 
                                    iqvdataSummary=obj_in.iqvdataSummary,
                                    iqvdata=obj_in.iqvdata, )
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as ex:
            db.rollback()
        return db_obj

    def update(
            self, db: Session, *, db_obj: PD_Protocol_Data, obj_in: Union[ProtocolDataUpdate, Dict[str, Any]]
    ) -> PD_Protocol_Data:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


pd_protocol_data = CRUDProtocolData(PD_Protocol_Data)
