from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pd_document_compare import PD_Document_Compare
from app.schemas.pd_document_compare import DocumentCompareCreate, DocumentCompareUpdate, DocumentCompare


class CRUDDocumentCompare(CRUDBase[PD_Document_Compare, DocumentCompareCreate, DocumentCompareUpdate]):
    def get_by_compareId(self, db: Session, *, compareId: Any) -> Optional[PD_Document_Compare]:
        return db.query(PD_Document_Compare).filter(PD_Document_Compare.compareId == compareId).first()

    def create(self, db: Session, *, obj_in: DocumentCompareCreate) -> PD_Document_Compare:
        db_obj = PD_Document_Compare(compareId=obj_in.compareId,
                                    id1=obj_in.id1,
                                    protocolNumber=obj_in.protocolNumber,
                                    projectId=obj_in.projectId,
                                    versionNumber=obj_in.versionNumber,
                                    amendmentNumber=obj_in.amendmentNumber,
                                    documentStatus=obj_in.documentStatus,
                                    id2=obj_in.id2, 
                                    protocolNumber2=obj_in.protocolNumber2,
                                    projectId2=obj_in.projectId2, 
                                    versionNumber2=obj_in.versionNumber2,
                                    amendmentNumber2=obj_in.amendmentNumber2,
                                    documentStatus2=obj_in.documentStatus2,
                                    environment=obj_in.environment,
                                    sourceSystem=obj_in.sourceSystem,
                                    userId=obj_in.userId,
                                    requestType=obj_in.requestType,
                                    iqvdata=obj_in.iqvdata,
                                    baseIqvXmlPath=obj_in.baseIqvXmlPath,
                                    compareIqvXmlPath=obj_in.compareIqvXmlPath,
                                    updatedIqvXmlPath=obj_in.updatedIqvXmlPath,
                                    similarityScore=obj_in.similarityScore, )
        
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as ex:
            db.rollback()
        return db_obj

    def update(
            self, db: Session, *, db_obj: PD_Document_Compare, obj_in: Union[DocumentCompareUpdate, Dict[str, Any]]
    ) -> PD_Document_Compare:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_by_docId(self, db: Session, id1: Any, id2: Any) -> Optional[PD_Document_Compare]:
        return db.query(PD_Document_Compare).filter(PD_Document_Compare.id1 == id1).filter(PD_Document_Compare.id2 == id2).first()


pd_document_compare = CRUDDocumentCompare(PD_Document_Compare)
