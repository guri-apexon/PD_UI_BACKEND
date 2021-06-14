from datetime import datetime, timedelta
from typing import Any, Optional, Union, Dict

from app.crud.base import CRUDBase
from app.models.pd_protocol_alert import ProtocolAlert
from app.models.pd_user_protocols import PD_User_Protocols
from app import schemas
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.utilities.config import settings


class CRUDUserAlert(CRUDBase[ProtocolAlert, schemas.UserAlertInput, schemas.UserAlert]):
    def get_by_userid(self, db: Session, *, user_id: Any) -> Optional[ProtocolAlert]:
        alert_from_time = datetime.utcnow() + timedelta(days = settings.ALERT_FROM_DAYS)
        return db.query(ProtocolAlert
                ).join(PD_User_Protocols, and_(PD_User_Protocols.userId == user_id, PD_User_Protocols.follow == True, PD_User_Protocols.id == ProtocolAlert.id)
                ).filter(ProtocolAlert.timeCreated > alert_from_time
                ).all()

pd_user_alert = CRUDUserAlert(ProtocolAlert)
