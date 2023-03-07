import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.pd_user_protocols import PD_User_Protocols
from app.models.pd_protocol_alert import ProtocolAlert
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

    from_days_no = 45
    get_45_days_before_date = datetime.datetime.utcnow() - datetime.timedelta(days=from_days_no)
    unique_protocols_user_opted = db.query(PD_User_Protocols).filter(PD_User_Protocols.userId == user_id).distinct(PD_User_Protocols.protocol).all()
    protocol_list = [item.protocol for item in unique_protocols_user_opted]
    notofication_query = db.query(ProtocolAlert).filter(ProtocolAlert.protocol.in_(protocol_list), ProtocolAlert.timeUpdated >= get_45_days_before_date, ProtocolAlert.isActive == True)
    notofication_list = [{"id":record.id, "protocol":record.protocol, 
                            "protocolTitle":record.protocolTitle,"readFlag":record.readFlag,
                            "doc_id":record.aidocId} for record in notofication_query]
    logger.info(f"fetching all notification for user_id {user_id}") 
    return notofication_list

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
            db.query(ProtocolAlert).filter(ProtocolAlert.id == id, ProtocolAlert.protocol == protocol, ProtocolAlert.aidocId == aidocId).update({ProtocolAlert.isActive: False})
            logger.info(f"notification record update isActive to False for doc_id {aidocId}, id {id} and protocol {protocol}")
        elif action == "read":
            db.query(ProtocolAlert).filter(ProtocolAlert.id == id, ProtocolAlert.protocol == protocol, ProtocolAlert.aidocId == aidocId).update({ProtocolAlert.readFlag: True})
            logger.info(f"notification record update readflag to True for doc_id {aidocId}, id {id} and protocol {protocol}")
            
        db.commit()
        return {"status":"success","id":id}
    except Exception as ex:
        logger.exception(f"exception occured to {action} the notification ,doc_id {aidocId}, id {id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Exception to read/delete notification {str(ex)}")