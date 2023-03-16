import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.pd_protocol_alert import ProtocolAlert
from app.models.pd_user_notification_type import PdUserNotificationType
from sqlalchemy.engine import Row
import logging
from app.utilities.config import settings
from app.utilities.email.send_mail import qc_complete_mail


logger = logging.getLogger(settings.LOGGER_NAME)

def get_notifications_from_db(db:Session  ,user_id:str) -> list:
    
    """
    Get all notification for user 
    :param user_id: user id to fetch notification
    :param db: database instance
    filtering for notifications created since 45 days old
    """

    start_period_timestamp = datetime.datetime.utcnow() - datetime.timedelta(days=settings.NOTIFICATION_ALERT_FROM_DAYS)
    notification_query = db.query(PdUserNotificationType).filter(
                                    PdUserNotificationType.created_time  >= start_period_timestamp,
                                    PdUserNotificationType.read_flag == False,
                                    PdUserNotificationType.notification_delete == False,
                                    PdUserNotificationType.userId == user_id
                                )
    notification_list = [{"id": record.id, "protocol": eval(record.content).get("protocol",""),
                          "protocolTitle": eval(record.content).get("protocolTitle",""),
                          "readFlag": record.read_flag, "doc_id": eval(record.content).get("doc_id",""),
                          "timestamp": record.created_time} for record in
                         notification_query]
    logger.info(f"fetching all notification for user_id {user_id}") 
    return notification_list

def create_notification_record_and_send_email(db: Session, metadata_resource: Row, event: str = "QC Complete") -> dict:
    """
    Create Notification record after QC Approve
    :param db: db instance
    :metadata_resource: ProtocolAlert table column 
    """
    pd_alert_obj = ProtocolAlert(
        aidocId = metadata_resource.aidocId,
        protocol = metadata_resource.protocol,
        protocolTitle = metadata_resource.protocolTitle + event,
    )
    db.add(pd_alert_obj)
    db.commit()
    db.refresh(pd_alert_obj)
    qc_complete_mail(db, pd_alert_obj.aidocId)
    logger.info(f"notification record created at protocol_alert table for QC complete for doc_id {metadata_resource.aidocId}")

    return {"id":pd_alert_obj.id}

def read_or_delete_notification(db: Session, aidocId: str, id: str, protocol: str, action: str) -> dict:
    try:
        if action == "delete":
            db.query(PdUserNotificationType).filter(PdUserNotificationType.id == id).update({PdUserNotificationType.notification_delete: True})
            logger.info(f"notification record update isActive to False for doc_id {aidocId}, id {id} and protocol {protocol}")
        elif action == "read":
            db.query(PdUserNotificationType).filter(PdUserNotificationType.id == id).update({PdUserNotificationType.read_flag: True})
            logger.info(f"notification record update readflag to True for doc_id {aidocId}, id {id} and protocol {protocol}")
        db.commit()
        return {"status":"success","id":id}
    except Exception as ex:
        logger.exception(f"exception occured to {action} the notification ,doc_id {aidocId}, id {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Exception to read/delete notification {str(ex)}")