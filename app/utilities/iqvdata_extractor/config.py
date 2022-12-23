import logging

from app.utilities.iqvdata_extractor import Constants, configuration

logger = logging.getLogger(Constants.MICROSERVICE_NAME)


class Config:

    PIPELINE_SERVICE_NAMES = ["triage",
                              "digitizer",
                              "classifier",
                              "metadata_extraction",
                              "finalization"
                              ]

    COMPOSITE_SCORE_WEIGHTS = {
        "classification": 0.7,
        "date": 0.1,
        "language": 0.1,
        "subject": 0.1
    }

    CONFIDENCE_SCORES = {}
    CONFIDENCE_SCORE_MEANS = {}

    FEEDBACK_XML_PREFIX = 'feedback_'

    FALL_BACK_DATE = None
    EXPIRATION_DATE = "Expiration Date"
    LAST_ENTRY_DATE = "Last Entry Date"
    ALIAS_GUIDANCE = "alternate_guidance"
    SECONDARY_GUIDANCE = "secondary_guidance"


class Alcoac:
    class ErrorCode:
        DUPLICATE_DOCUMENT = "duplicate_document_error"
        FILE_TYPE = "filetype_error"
        BLANK_PAGES = "blank_pages_error"
        PAGE_SKEW = "page_skew_error"
        GRAYSCALE = "greyscale_error"
        LEGIBILITY = "legibility_error"
        MISSING_PAGES = "missing_pages_error"
        ORDER_PAGES = "order_pages_error"

    class IqvxmlCode:
        ALCOAC_ERROR_MESSAGE = "alcoac_error_message"
        ALCOAC_ERROR_SCORE = "alcoac_error_score"
        ALCOAC_ERROR_CONF = "alcoac_error_confidence"

    DISPLAY_ERROR = {
        # single item, string, pre-formatted from mgmt service,  example - Document previously uploaded by
        # user: {user_id}, at time: {time_created} with file name: {file_name}, having id: {duplicate_resource_id}
        ErrorCode.DUPLICATE_DOCUMENT: "{}",

        # single item, string, file extension, example - .xyz
        ErrorCode.FILE_TYPE: "Document file type {} not supported",

        # multiple items, string, page number, example - '3'
        ErrorCode.BLANK_PAGES: "Blank page(s) {}",

        # multiple items, string, page number, example - '5'
        ErrorCode.PAGE_SKEW: "Orientation issue on page(s) {}",

        # multiple items, string, page number, example - '3'
        ErrorCode.GRAYSCALE: "Legibility issue on page(s) {}",

        # multiple items, string, page number, example - '5'
        ErrorCode.LEGIBILITY: "Legibility issue on page(s) {}",

        # single item, string, list of extracted pages, example - '[1, 2, 5]'
        ErrorCode.MISSING_PAGES: "Missing pages, extracted page(s) {}",

        # single item, string, list of extracted pages, example - '[1, 3, 2]'
        ErrorCode.ORDER_PAGES: "Pagination issue, extracted page(s) {}"
    }
