from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pd_recent_search import PD_Protocol_Recent_Search
from app.schemas.pd_recent_search import RecentSearchCreate, RecentSearchUpdate, RecentSearch


class CRUDRecentSearch(CRUDBase[PD_Protocol_Recent_Search, RecentSearchCreate, RecentSearchUpdate]):
    def get_by_id(self, db: Session, *, search_id: int) -> Optional[PD_Protocol_Recent_Search]:
        return db.query(PD_Protocol_Recent_Search).filter(PD_Protocol_Recent_Search.id == search_id).first()

    def create(self, db: Session, *, obj_in: RecentSearchCreate) -> PD_Protocol_Recent_Search:
        db_obj = PD_Protocol_Recent_Search(keyword=obj_in.keyword,
                                        user=obj_in.user,
                                        timeCreated=obj_in.timeCreated,
                                        lastUpdated=obj_in.lastUpdated, )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
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
