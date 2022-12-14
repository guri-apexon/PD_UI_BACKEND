class ErrorCodes:
    UNKNOWN_ERROR = 500
    FEEDBACK_PROCESS_XML_WRITING_FAILURE = 501
    FETCHING_POST_ATTRIBUTES_FAILED = 507
    ALCOAC_VALUES_EXTRACTION_FAILED = 508
    WINGSPAN_MAPPING_FAILED = 509
    WRITING_FINALIZATION_FILE_FAILED = 510
    METRICS_EXTRACTION_FAILED = 511
    FETCHING_DOC_TYPE_FAILED = 520
    COMPOSITE_CONFIDENCE_GENERATION_FAILED = 522
    FETCHING_SITE_PERSONNEL_FAILED = 526
    FEEDBACK_PROCESS_XML_READING_FAILURE = 527
    FEEDBACK_PROCESS_INPUT_XML_NOT_FOUND = 528
    XML_READING_FAILURE = 529
    IQVDATA_FAILURE = 530


ERRORS = {
    ErrorCodes.UNKNOWN_ERROR: "Unknown error",
    ErrorCodes.FEEDBACK_PROCESS_XML_WRITING_FAILURE: "Error in feedback writing process",
    ErrorCodes.FEEDBACK_PROCESS_XML_READING_FAILURE: "Error in feedback reading process",
    ErrorCodes.FEEDBACK_PROCESS_INPUT_XML_NOT_FOUND: "Error in feedback - input xml is not found",
    ErrorCodes.FETCHING_POST_ATTRIBUTES_FAILED: "Error getting post attributes",
    ErrorCodes.ALCOAC_VALUES_EXTRACTION_FAILED: "Error in getting alcoac values",
    ErrorCodes.WINGSPAN_MAPPING_FAILED: "Error in mapping wingspan values",
    ErrorCodes.XML_READING_FAILURE: "Error during input XML reading process",
    ErrorCodes.WRITING_FINALIZATION_FILE_FAILED: "Error writing into finalization file",
    ErrorCodes.METRICS_EXTRACTION_FAILED: "Error during metrics extraction",
    ErrorCodes.FETCHING_DOC_TYPE_FAILED: "Error in getting doc type",
    ErrorCodes.COMPOSITE_CONFIDENCE_GENERATION_FAILED: "Error in composite confidence",
    ErrorCodes.FETCHING_SITE_PERSONNEL_FAILED: "Error fetching site personnel details",
    ErrorCodes.IQVDATA_FAILURE: "Error reading iqvdocument"
}


class FinalizationException(Exception):

    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = ERRORS[error_code]
        self.error_message_details = error_message

    def __str__(self):
        return f'({self.error_code}, {self.error_message}, {self.error_message_details})'
