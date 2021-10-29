from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session
import logging
from app.crud.base import CRUDBase
from app.models.pd_document_compare import PD_Document_Compare
from app.utilities.config import settings
from app.schemas.pd_document_compare import DocumentCompareCreate, DocumentCompareUpdate, DocumentCompare

from fastapi import status, HTTPException

logger = logging.getLogger(settings.LOGGER_NAME)

class CRUDDocumentCompare(CRUDBase[PD_Document_Compare, DocumentCompareCreate, DocumentCompareUpdate]):

    def get_compare_path(self, db: Session, id1: Any, id2: Any, redact_profile: Any) -> Optional[PD_Document_Compare]:
        try:
            resource = db.query(PD_Document_Compare).filter(PD_Document_Compare.id1 == id1,
                                                                    PD_Document_Compare.id2 == id2, 
                                                                    PD_Document_Compare.redactProfile == redact_profile).all()
            if not resource:
                logger.exception(f'No Document Found for id1:{id1} and id2:{id2} in pd_protocol_compare Table.')
                raise HTTPException(status_code=404, detail=f"No Document Found for id1:{id1} and id2:{id2} in pd_protocol_compare Table.")

            compare_record = max(resource, key = lambda record : record.compareRun)
            return compare_record

        except Exception as ex:
            logger.exception(f'Exception occured during pulling of data from db {str(ex)}')


pd_document_compare = CRUDDocumentCompare(PD_Document_Compare)
