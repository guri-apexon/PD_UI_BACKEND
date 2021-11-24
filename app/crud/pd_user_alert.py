from datetime import datetime, timedelta
from typing import Any

from app.crud.base import CRUDBase
from app.models.pd_protocol_alert import ProtocolAlert
from app.models.pd_user_protocols import PD_User_Protocols
from app.models.pd_protocol_metadata import PD_Protocol_Metadata
from app import schemas
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.utilities.config import settings
from http import HTTPStatus
import logging
from app import config
from app.utilities.redact import redactor
from app.db.session import SessionLocal

logger = logging.getLogger(settings.LOGGER_NAME)
db = SessionLocal()


class CRUDUserAlert(CRUDBase[ProtocolAlert, schemas.UserAlertInput, schemas.UserAlert]):
    def get_by_userid(self, db: Session, *, user_id: Any, alert_from_days=settings.ALERT_FROM_DAYS):
        alert_from_time = datetime.utcnow() + timedelta(days=alert_from_days)

        user_alerts = db.query(ProtocolAlert, PD_Protocol_Metadata.uploadDate) \
            .join(PD_User_Protocols, and_(PD_User_Protocols.userId == user_id,
                                          PD_User_Protocols.follow == True,
                                          PD_User_Protocols.id == ProtocolAlert.id)) \
            .join(PD_Protocol_Metadata, and_(PD_Protocol_Metadata.id == ProtocolAlert.aidocId,
                                             PD_Protocol_Metadata.protocol == ProtocolAlert.protocol)) \
            .filter(ProtocolAlert.timeCreated > alert_from_time).all()

        for user_alert, protocol_upload_date in user_alerts:
            profile_name, profile_details, _ = redactor.get_current_redact_profile(current_db=db,
                                                                                   user_id=user_id,
                                                                                   protocol=user_alert.protocol)

            for attr_name in profile_details.get(config.GENRE_ATTRIBUTE_ENTITY, []):
                if attr_name in user_alert.__dict__:
                    doc_attributes = {"AiDocId": user_alert.aidocId,
                                      attr_name: user_alert.__getattribute__(attr_name),
                                      "uploadDate": protocol_upload_date}
                    redacted_doc_attributes = redactor.redact_protocolTitle(current_db=db,
                                                                            attribute=attr_name,
                                                                            profile=profile_details,
                                                                            doc_attributes=doc_attributes,
                                                                            redact_flg=config.REDACTION_FLAG[profile_name])
                    user_alert.__setattr__(attr_name, redacted_doc_attributes[attr_name])
        user_alerts = [user_alert[0] for user_alert in user_alerts]
        return user_alerts

    def update_notification_read_status(self, notification_read_in: schemas.NotificationRead, db):
        try:
            if notification_read_in.aidocId == '' or notification_read_in.id == '':
                logger.error("Got aidocid: {} and id: {} in update_notification_read_status.".format(notification_read_in.aidocId, notification_read_in.id))
                res = dict()
                res['ResponseCode'] = HTTPStatus.NOT_ACCEPTABLE
                res['Message'] = "Got aidocid: {} and id: {} in update_notification_read_status.".format(notification_read_in.aidocId, notification_read_in.id)
                return res

            protocol_alert = db.query(ProtocolAlert).filter(and_(ProtocolAlert.aidocId == notification_read_in.aidocId,
                                                                 ProtocolAlert.id == notification_read_in.id,
                                                                 ProtocolAlert.protocol == notification_read_in.protocol)).first()
            if protocol_alert:
                time_ = datetime.utcnow()
                protocol_alert.readFlag = True
                protocol_alert.readTime = time_
                protocol_alert.timeUpdated = time_
                db.add(protocol_alert)
                db.commit()
                res = {'ResponseCode': HTTPStatus.OK, 'Message': 'Success'}
            else:
                logger.info("Entry for {} not found in db to update pd_protocol_alert notification read.".format(notification_read_in.aidocId))
                res = dict()
                res['ResponseCode'] = HTTPStatus.NO_CONTENT
                res['Message'] = 'Entry for {} not found in db to update pd_protocol_alert notification read.'.format(notification_read_in.aidocId)

        except Exception as ex:
            logger.exception("Exception Inside update_notification_read_status", ex)
            res = dict()
            res['ResponseCode'] = HTTPStatus.INTERNAL_SERVER_ERROR
            res['Message'] = str(ex)
        return res


pd_user_alert = CRUDUserAlert(ProtocolAlert)
