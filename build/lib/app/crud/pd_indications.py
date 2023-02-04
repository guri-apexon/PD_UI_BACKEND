from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pd_indications import PD_Protocol_Indication
from app.schemas.pd_indications import IndicationsCreate, IndicationsUpdate, Indications


class CRUDPDIndications(CRUDBase[PD_Protocol_Indication, IndicationsCreate, IndicationsUpdate]):
    def get_by_id(self, db: Session, *, indId: int) -> Optional[PD_Protocol_Indication]:
        return db.query(PD_Protocol_Indication).filter(PD_Protocol_Indication.indId == indId).first()

    def get_all_indications_sorted(
        self, db: Session) -> List[PD_Protocol_Indication]:
        """Retrieves all records by default and limit can be set"""
        return db.query(self.model).order_by(self.model.indicationName).all()


    def create(self, db: Session, *, obj_in: IndicationsCreate) -> PD_Protocol_Indication:
        db_obj = PD_Protocol_Indication(indicationName=obj_in.indicationName, )
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as ex:
            db.rollback()
        return db_obj

    def update(
            self, db: Session, *, db_obj: PD_Protocol_Indication, obj_in: Union[IndicationsUpdate, Dict[str, Any]]
    ) -> PD_Protocol_Indication:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


pd_indication = CRUDPDIndications(PD_Protocol_Indication)
