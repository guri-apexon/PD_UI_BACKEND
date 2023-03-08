import logging
import uuid
from app.crud.base import CRUDBase
from app.utilities.config import settings
from app.models.pd_user_protocols_access import PDUserAccessChangeLog
from app.schemas.pd_user_protocols_access import UserProtocolAccessCreate, \
    UserProtocolAccessUpdate
from sqlalchemy.orm import Session
from app import config

logger = logging.getLogger(settings.PROJECT_NAME)


class CRUDUserProtocolsAccess(CRUDBase[PDUserAccessChangeLog, UserProtocolAccessCreate, UserProtocolAccessUpdate]):

    @staticmethod
    def add_data_to_db(db: Session, existing_role, protocol_access):
        """ Capture user access level changes log into DB """
        new_user_role = protocol_access.userRole
        access_level_change = f'{existing_role} to {new_user_role}'
        redact_profile = config.USERROLE_REDACTPROFILE_MAP.get(new_user_role,
                                                               "profile_0")

        change_log_obj = PDUserAccessChangeLog(id=str(uuid.uuid1()),
                                               userId=protocol_access.userId,
                                               protocol=protocol_access.protocol,
                                               projectId=protocol_access.projectId,
                                               follow=protocol_access.follow,
                                               userRole=protocol_access.userRole,
                                               redactProfile=redact_profile,
                                               userUpdated=protocol_access.userUpdated,
                                               reason_for_change=protocol_access.accessReason,
                                               access_level_change=access_level_change
                                               )
        try:
            db.add(change_log_obj)
            db.commit()
            db.refresh(change_log_obj)
        except Exception as ex:
            db.rollback()
            logger.error(f"Exception received for userID: "
                         f"{protocol_access.userId} and \n ERROR Details: {str(ex)}")
        return change_log_obj


pd_user_protocols_access = CRUDUserProtocolsAccess(PDUserAccessChangeLog)
