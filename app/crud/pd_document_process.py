from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pd_document_process import PD_Document_Process
from app.schemas.pd_document_process import DocumentProcessCreate, DocumentProcessUpdate, DocumentProcess


class CRUDDocumentProcess(CRUDBase[PD_Document_Process, DocumentProcessCreate, DocumentProcessUpdate]):
    def get_by_id(self, db: Session, *, id: Any) -> Optional[PD_Document_Process]:
        return db.query(PD_Document_Process).filter(PD_Document_Process.id == id).first()

    def create(self, db: Session, *, obj_in: DocumentProcessCreate) -> PD_Document_Process:
        db_obj = PD_Document_Process(id=obj_in.id,
                                    userId=obj_in.userId,
                                    isProcessing=obj_in.isProcessing,
                                    fileName=obj_in.fileName,
                                    documentFilePath=obj_in.documentFilePath,
                                    percentComplete=obj_in.percentComplete,
                                    status=obj_in.status,
                                    feedback=obj_in.feedback, 
                                    errorCode=obj_in.errorCode,
                                    errorReason=obj_in.errorReason, 
                                    timeCreated=obj_in.timeCreated,
                                    lastUpdated=obj_in.lastUpdated, )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: PD_Document_Process, obj_in: Union[DocumentProcessUpdate, Dict[str, Any]]
    ) -> PD_Document_Process:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


pd_document_process = CRUDDocumentProcess(PD_Document_Process)
