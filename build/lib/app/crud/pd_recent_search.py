from typing import Any, Dict, Optional, Union, List

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pd_recent_search import PD_Protocol_Recent_Search
from app.schemas.pd_recent_search import RecentSearchCreate, RecentSearchUpdate, RecentSearch


class CRUDRecentSearch(CRUDBase[PD_Protocol_Recent_Search, RecentSearchCreate, RecentSearchUpdate]):
    def get_by_id(self, db: Session, *, sponsorId: int) -> Optional[PD_Protocol_Recent_Search]:
        return db.query(PD_Protocol_Recent_Search).filter(PD_Protocol_Recent_Search.sponsorId == sponsorId).first()

    def get_recent_search_by_userId(self, db: Session, userId: str) -> List[RecentSearch]:
        """Retrieves a record based on primary key or id"""
        return db.query(self.model).filter(self.model.userId == userId).order_by(desc(self.model.timeCreated)).\
            limit(20).all()

    def create(self, db: Session, *, obj_in: RecentSearchCreate) -> PD_Protocol_Recent_Search:
        db_obj = PD_Protocol_Recent_Search(keyword=obj_in.keyword,
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
            self, db: Session, *, db_obj: PD_Protocol_Recent_Search, obj_in: Union[RecentSearchUpdate, Dict[str, Any]]
    ) -> PD_Protocol_Recent_Search:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


pd_recent_search = CRUDRecentSearch(PD_Protocol_Recent_Search)
