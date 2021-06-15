from datetime import datetime, timedelta
from typing import Any, Optional, Union, Dict

from app.crud.base import CRUDBase
from app.models.pd_protocol_alert import ProtocolAlert
from app.models.pd_user_protocols import PD_User_Protocols
from app import schemas
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.utilities.config import settings
from http import HTTPStatus
import logging

logger = logging.getLogger(settings.LOGGER_NAME)


class CRUDUserAlert(CRUDBase[ProtocolAlert, schemas.UserAlertInput, schemas.UserAlert]):
    def get_by_userid(self, db: Session, *, user_id: Any) -> Optional[ProtocolAlert]:
        alert_from_time = datetime.utcnow() + timedelta(days = settings.ALERT_FROM_DAYS)
        return db.query(ProtocolAlert
                ).join(PD_User_Protocols, and_(PD_User_Protocols.userId == user_id, PD_User_Protocols.follow == True, PD_User_Protocols.id == ProtocolAlert.id)
                ).filter(ProtocolAlert.timeCreated > alert_from_time
                ).all()


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
