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

    @staticmethod
    def prepare_response(obj_in: UserAlertSetting):
        """ To prepare user setting response with options separately """
        return {
            "userId": obj_in.userId,
            "id": obj_in.id,
            "created_time": obj_in.created_time,
            "updated_time": obj_in.updated_time,
            "options": {
                "QC_Complete": obj_in.QC_complete,
                "New_Document/Version": obj_in.new_document_version,
                "Edited": obj_in.edited
            }
        }

    def get_user_options(self, db: Session, user_id: str):
        """ To get user alert global setting """
        user_obj = self.get_by_user_id(db=db, user_id=user_id)
        user_options = self.prepare_response(user_obj)
        return user_options

    def update_user_alert_setting(self, db: Session, obj_in: UserAlertSetting):
        """
        Update existing user with user alert settings
        """
        user_id = obj_in.userId
        alert_rec = self.get_by_user_id(db=db, user_id=user_id)
        if not alert_rec:
            return False
        else:
            alert_rec.new_document_version = obj_in.options.get(
                'New_Document/Version', False)
            alert_rec.edited = obj_in.options.get('Edited', False)
            alert_rec.QC_complete = obj_in.options.get('QC_Complete', False)
            alert_rec.updated_time = datetime.utcnow()
            try:
                db.add(alert_rec)
                db.commit()
                db.refresh(alert_rec)
            except Exception as ex:
                db.rollback()
                logger.error(
                    f"Exception received for userID: {user_id} ERROR Details: {str(ex)}")
        user_options = self.prepare_response(alert_rec)
        return user_options


user_alert_setting = CRUDUserAlertSetting(UserAlertSetting)
