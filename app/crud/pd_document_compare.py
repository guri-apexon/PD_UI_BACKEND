from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pd_document_compare import PD_Document_Compare
from app.schemas.pd_document_compare import DocumentCompareCreate, DocumentCompareUpdate, DocumentCompare

class CRUDDocumentCompare(CRUDBase[PD_Document_Compare, DocumentCompareCreate, DocumentCompareUpdate]):

    def get_compare_path(self, db: Session, id1: Any, id2: Any) -> Optional[PD_Document_Compare]:
        return db.query(PD_Document_Compare).filter(PD_Document_Compare.id1 == id1,
                                                        PD_Document_Compare.id2 == id2).first()

pd_document_compare = CRUDDocumentCompare(PD_Document_Compare)
