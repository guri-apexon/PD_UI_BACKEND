import logging
from datetime import datetime

from app.utilities.config import settings
from app.models.pd_user_alert_setting import UserAlertSetting
from app.schemas.pd_user_alert_setting import UserAlertSettingCreate, \
    UserAlertSettingUpdate
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session

logger = logging.getLogger(settings.LOGGER_NAME)


class CRUDUserAlertSetting(CRUDBase[UserAlertSetting, UserAlertSettingCreate, UserAlertSettingUpdate]):

    @staticmethod
    def get_by_user_id(db: Session, user_id: str):
        return db.query(UserAlertSetting).filter(
            UserAlertSetting.userId == user_id).first()

    def update_user_alert_setting(self, db: Session, obj_in: UserAlertSetting):
        """
        Update existing user with user alert settings
        """
        user_id = obj_in.userId
        alert_rec = self.get_by_user_id(db=db, user_id=user_id)
        if not alert_rec:
            return False
        else:
            alert_rec.new_document_version = True if 'new_document_version' in obj_in.options else False
            alert_rec.edited = True if 'edited' in obj_in.options else False
            alert_rec.QC_complete = True if 'QC_complete' in obj_in.options else False
            alert_rec.updated_time = datetime.utcnow()
            try:
                db.add(alert_rec)
                db.commit()
                db.refresh(alert_rec)
            except Exception as ex:
                db.rollback()
                logger.error(
                    f"Exception received for userID: {user_id} ERROR Details: {str(ex)}")
        return alert_rec


user_alert_setting = CRUDUserAlertSetting(UserAlertSetting)
