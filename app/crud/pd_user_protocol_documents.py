from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pd_user_protocol_documents import PD_User_Protocol_Documents
from app.schemas.pd_user_protocol_documents import UserProtocolDocumentsCreate, UserProtocolDocumentsUpdate


class CRUDUserProtocolDocuments(CRUDBase[PD_User_Protocol_Documents, UserProtocolDocumentsCreate,
                                         UserProtocolDocumentsUpdate]):

    def get_by_id(self, db: Session, *, user_protocol_document_id: int) -> Optional[PD_User_Protocol_Documents]:
        return db.query(PD_User_Protocol_Documents).filter(PD_User_Protocol_Documents.id ==
                                                           user_protocol_document_id).first()

    def create(self, db: Session, *, obj_in: UserProtocolDocumentsCreate) -> PD_User_Protocol_Documents:
        db_obj = PD_User_Protocol_Documents(protocol_id=obj_in.protocol_id,
                                            user_id=obj_in.user_id,
                                            protocol_document_name=obj_in.protocol_document_name,
                                            protocol_document_status_id=obj_in.protocol_document_status_id,
                                            protocol_source_document_id=obj_in.protocol_source_document_id,
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
            self, db: Session, *, db_obj: PD_User_Protocol_Documents, obj_in: Union[UserProtocolDocumentsUpdate,
                                                                                    Dict[str, Any]]
    ) -> PD_User_Protocol_Documents:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


pd_user_protocol_document = CRUDUserProtocolDocuments(PD_User_Protocol_Documents)
