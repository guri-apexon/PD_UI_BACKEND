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
@unique
class QcStatus(Enum):
    """PD Quality Check status"""
    NOT_STARTED = 'QC_NOT_STARTED'
    QC1 = 'QC1'
    QC2 = 'QC2'
    COMPLETED = 'QC_COMPLETED'

VALID_QC_STATUS = [status.value for status in QcStatus]

OVERRIDE_QC_FIELDS = ()

# -------------- Misc
DIGITIZATION_COMPLETED_STATUS = "PROCESS_COMPLETED"
QC_COMPLETED_STATUS = QcStatus.COMPLETED.value

# Redaction profile
USERROLE_REDACTPROFILE_MAP = {"primary": "profile_1", "secondary": "profile_0", "default": "profile_0"}

GENRE_ENTITY_NAME = 'entity'
GENRE_ATTRIBUTE_NAME = 'attributes'
GENRE_ACTION_NAME = 'action'
GENRE_SECTION_NAME = 'section'

# Redaction Footnotes
FOOTNOTES_TEXT = "Text"
FOOTNOTES_ENTITIES = "entities"
FOOTNOTES_START_INDEX = "start_idx"
FOOTNOTES_END_INDEX = "end_idx"
FOOTNOTES_KEY = "Key"
FOOTNOTE_STR = "FootnoteText"

SRC_DOC_ACTION_TYPE = 'download_source_document'
COMPARED_DOC_ACTION_TYPE = 'download_compare_document'
