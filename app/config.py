import re
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
    FEEDBACK = 'FEEDBACK_RUN'
    COMPLETED = 'QC_COMPLETED'
    QC = 'QC'

VALID_QC_STATUS = [status.value for status in QcStatus]

OVERRIDE_QC_FIELDS = ()

# -------------- Misc
DIGITIZATION_COMPLETED_STATUS = "PROCESS_COMPLETED"
QC_APPROVED_STATUS = QcStatus.FEEDBACK.value
QC_COMPLETED_STATUS = QcStatus.COMPLETED.value

# ---------------------- Redaction
# Profiles
USERROLE_REDACTPROFILE_MAP = {"primary": "profile_1", "secondary": "profile_0", "default": "profile_0"}
REGEX_SPECIAL_CHAR_REPLACE = re.compile('([\(\)\[\]])')

GENRE_ENTITY_NAME = 'entity'
GENRE_ATTRIBUTE_NAME = 'attributes'
GENRE_ACTION_NAME = 'action'
GENRE_SECTION_NAME = 'section'
GENRE_ATTRIBUTE_ENTITY = "attributes_entity"
REDACT_ATTR_STR = '~REDACTED~'
REDACT_PARAGRAPH_STR = '~REDACTED~'

# Redaction
REDACTION_FLAG = {"profile_1": False, "profile_0": True}
EXCLUDE_REDACT_PROPERTY_FLAG = {"profile_1": False, "profile_0": True}
HIDE_TABLE_JSON_FLAG = {"profile_1": True, "profile_0": True}
RETURN_REFRESHED_TABLE_HTML_FLAG = {"profile_1": False, "profile_0": True}

# File prefix
QC_WIP_SRC_DB_FILE_PREFIX = "WIP_SRC_DB"
QC_WIP_SRC_QC_FILE_PREFIX = "WIP_SRC_QC"
QC_APPROVED_FILE_PREFIX = "QC"
DIG_FILE_PREFIX = "DIG"

START_INDEX_PATTERN = "start_idx"
END_INDEX_PATTERN = "end_idx"

# Redaction Footnotes
FOOTNOTES_TEXT = "Text"
FOOTNOTES_ENTITIES = "entities"
FOOTNOTES_START_INDEX = "start_idx"
FOOTNOTES_END_INDEX = "end_idx"
FOOTNOTES_KEY = "Key"
FOOTNOTE_STR = "FootnoteText"

SRC_DOC_ACTION_TYPE = 'download_source_document'
COMPARED_DOC_ACTION_TYPE = 'download_compare_document'

# Regex for
REGEX_EMP_ID_ALPHA_REPLACE = re.compile('^[a-zA-Z]+')

# Value for QC
QC = 'QC'

