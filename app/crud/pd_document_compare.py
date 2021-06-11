from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
import logging
from app.crud.base import CRUDBase
from app.models.pd_document_compare import PD_Document_Compare
from app.utilities.config import settings
from app.schemas.pd_document_compare import DocumentCompareCreate, DocumentCompareUpdate, DocumentCompare
logger = logging.getLogger(settings.LOGGER_NAME)

class CRUDDocumentCompare(CRUDBase[PD_Document_Compare, DocumentCompareCreate, DocumentCompareUpdate]):

    def get_compare_path(self, db: Session, id1: Any, id2: Any) -> Optional[PD_Document_Compare]:
        try:
            compare_record = db.query(PD_Document_Compare).filter(PD_Document_Compare.id1 == id1,
                                                            PD_Document_Compare.id2 == id2).first()
            return compare_record
        except Exception as ex:
            logger.exception(f'Exception occured during pulling of data from db {str(ex)}')
pd_document_compare = CRUDDocumentCompare(PD_Document_Compare)
