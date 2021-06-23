from enum import Enum, unique

# -------- User roles
@unique
class UserRole(Enum):
    """User Roles"""
    PRIMARY = 'primary'
    NON_PRIMARY = 'secondary'

# -------- Follow/Unfollow 
FOLLOW_DEFAULT_ROLE = UserRole.NON_PRIMARY.value
FOLLOW_ALLOWED_ROLES = [role.value for role in UserRole]

# --------  QC status
# VALID_QC_STATUS = ('QC_NOT_STARTED', 'QC1', 'QC2', 'QC_COMPLETED')
@unique
class QcStatus(Enum):
    """PD Quality Check status"""
    NOT_STARTED = 'QC_NOT_STARTED'
    QC1 = 'QC1'
    QC2 = 'QC2'
    COMPLETED = 'QC_COMPLETED'

qc_status_all = [status.value for status in QcStatus]

OVERRIDE_QC_FIELDS = ()
# -------------- Misc
DIGITIZATION_COMPLETED_STATUS = "PROCESS_COMPLETED"