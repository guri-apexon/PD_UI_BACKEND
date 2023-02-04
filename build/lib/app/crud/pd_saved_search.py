from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pd_saved_search import PD_Protocol_Saved_Search
from app.schemas.pd_saved_search import SavedSearchCreate, SavedSearchUpdate, SavedSearch


class CRUDSavedSearch(CRUDBase[PD_Protocol_Saved_Search, SavedSearchCreate, SavedSearchUpdate]):
    def get_by_id(self, db: Session, *, saveId: int) -> Optional[PD_Protocol_Saved_Search]:
        return db.query(PD_Protocol_Saved_Search).filter(PD_Protocol_Saved_Search.saveId == saveId).first()

    def create(self, db: Session, *, obj_in: SavedSearchCreate) -> PD_Protocol_Saved_Search:
        db_obj = PD_Protocol_Saved_Search(keyword=obj_in.keyword,
                                        userId=obj_in.userId,
                                        timeCreated=obj_in.timeCreated,
                                        lastUpdated=obj_in.lastUpdated, )
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as ex:
            db.rollback()
        return db_obj

    def update(
            self, db: Session, *, db_obj: PD_Protocol_Saved_Search, obj_in: Union[SavedSearchUpdate, Dict[str, Any]]
    ) -> PD_Protocol_Saved_Search:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def get_by_userId(self, db: Session, userId: str) -> Optional[PD_Protocol_Saved_Search]:
        """Retrieves a record based on primary key or id"""
        return db.query(PD_Protocol_Saved_Search).filter(PD_Protocol_Saved_Search.userId == userId).order_by(PD_Protocol_Saved_Search.timeCreated.desc()).all()

pd_saved_search = CRUDSavedSearch(PD_Protocol_Saved_Search)
