import logging
from datetime import datetime
from typing import Optional

from app.crud.base import CRUDBase
from app.models.pd_redact_profile import PDRedactProfile
from app.schemas.pd_redact_profile import (RedactProfileCreate,
                                           RedactProfileUpdate)
from app.utilities.config import settings
from fastapi import HTTPException
from sqlalchemy.orm import Session

logger = logging.getLogger(settings.LOGGER_NAME)


class CRUDRedactProfile(CRUDBase[PDRedactProfile, RedactProfileCreate, RedactProfileUpdate]):
    def get_all_active(self, db: Session) -> Optional[PDRedactProfile]:
        """
        Retrieves all active redaction profile details
        """
        try:
            return db.query(PDRedactProfile).filter(PDRedactProfile.isActive == True).all()
        except Exception as exc:
            logger.exception(f"Exception in retrieval of active profiles: {str(exc)}")
            return None
  
pd_redact_profile = CRUDRedactProfile(PDRedactProfile)
