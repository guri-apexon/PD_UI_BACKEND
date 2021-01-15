from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pd_protocol_sponsor import PD_Protocol_Sponsor
from app.schemas.pd_protocol_sponsor import ProtocolSponsorCreate, ProtocolSponsorUpdate, ProtocolSponsor


class CRUDProtocolSponsor(CRUDBase[PD_Protocol_Sponsor, ProtocolSponsorCreate, ProtocolSponsorUpdate]):
    def get_by_id(self, db: Session, *, sponsorId: int) -> Optional[PD_Protocol_Sponsor]:
        return db.query(PD_Protocol_Sponsor).filter(PD_Protocol_Sponsor.sponsorId == sponsorId).first()

    def create(self, db: Session, *, obj_in: ProtocolSponsorCreate) -> PD_Protocol_Sponsor:
        db_obj = PD_Protocol_Sponsor(sponsorName=obj_in.sponsorName, )
        
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as ex:
            db.rollback()
        return db_obj

    def update(
            self, db: Session, *, db_obj: PD_Protocol_Sponsor, obj_in: Union[ProtocolSponsorUpdate, Dict[str, Any]]
    ) -> PD_Protocol_Sponsor:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


pd_protocol_sponsor = CRUDProtocolSponsor(PD_Protocol_Sponsor)
