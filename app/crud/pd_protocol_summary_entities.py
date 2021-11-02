from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.pd_protocol_summary_entiites import PDProtocolSummaryEntities
from app.schemas.pd_protocol_summary_entities import ProtocolSummaryEntitiesCreate, ProtocolSummaryEntitiesUpdate


class CRUDProtocols(CRUDBase[PDProtocolSummaryEntities, ProtocolSummaryEntitiesCreate, ProtocolSummaryEntitiesUpdate]):
    @staticmethod
    def get_protocol_summary_entities(db: Session, aidocId: Any) -> Optional[PDProtocolSummaryEntities]:
        """Retrieves a record based on primary key or id"""
        return db.query(PDProtocolSummaryEntities.aidocId,
                        PDProtocolSummaryEntities.source,
                        PDProtocolSummaryEntities.runId,
                        PDProtocolSummaryEntities.iqvdataSummaryEntities,
                        ).filter(PDProtocolSummaryEntities.aidocId == aidocId,
                                 PDProtocolSummaryEntities.isActive == True).first()

    def create(self, db: Session, *, obj_in: ProtocolSummaryEntitiesCreate) -> PDProtocolSummaryEntities:
        ...

    def update(
            self, db: Session, *, db_obj: PDProtocolSummaryEntities,
            obj_in: Union[ProtocolSummaryEntitiesUpdate, Dict[str, Any]]
    ) -> PDProtocolSummaryEntities:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


pd_protocol_summary_entities = CRUDProtocols(PDProtocolSummaryEntities)
