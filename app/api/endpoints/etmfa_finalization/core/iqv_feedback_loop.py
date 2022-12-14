import logging
import os

from etmfa_core.aidoc.io import read_iqv_xml, write_iqv_xml
from etmfa_core.aidoc.models.IQVDocument import (IQVDocument,
                                                 IQVDocumentFeedbackResults,
                                                 IQVKeyValueSet)
from etmfa_core.aidoc.models.IQVUtilities import GetDateTimeString
from etmfa_finalization import Constants
from etmfa_finalization.config import Config
from iqv_finalization_error import ErrorCodes, FinalizationException

logger = logging.getLogger(Constants.MICROSERVICE_NAME)


def read_iqvia_doc_for_feedback_update(root_folder: str) -> (str, IQVDocument):
    """Read latest IQVIA doc from the input folder."""
    full_paths = [os.path.join(root_folder, filename) for filename in os.listdir(root_folder)
                  if filename.endswith(".xml") or filename.endswith(".zip")]

    if not full_paths:
        raise FinalizationException(ErrorCodes.FEEDBACK_PROCESS_INPUT_XML_NOT_FOUND,
                                    f"IQVIA document is not present in {root_folder}")

    latest_file = max(full_paths, key=os.path.getmtime)  # Get the latest file from the directory

    try:
        iqvia_document = read_iqv_xml(latest_file)
    except Exception as e:
        raise FinalizationException(ErrorCodes.FEEDBACK_PROCESS_XML_READING_FAILURE, str(e))

    return latest_file, iqvia_document


def get_feedback_output_filename(feedback_input_file: str) -> str:
    """Get feedback filename."""
    filename = os.path.basename(feedback_input_file)

    if not filename.lower().startswith(Config.FEEDBACK_XML_PREFIX):
        filename = f"{Config.FEEDBACK_XML_PREFIX}{filename}"

    return filename


def populate_feedback_into_xml(feedback_request: dict):
    """Populate feedback results into IQVIA XML from provided feedback request dictionary."""
    root_folder = os.path.dirname(feedback_request['document_file_path'])
    feedback_input_file, doc = read_iqvia_doc_for_feedback_update(root_folder)
    feedback_output_path = os.path.join(root_folder, get_feedback_output_filename(feedback_input_file))
    feedback_results = IQVDocumentFeedbackResults()

    # TODO This check is temporary as we are getting Null represented as string from ui
    # (https://gitlabrnds.quintiles.com/etmf-group/etmfa-finalizer/issues/1)
    if feedback_request['attribute_auxillary_list'] != "null":
        for attributevalues in feedback_request['attribute_auxillary_list']:
            if attributevalues['name'] == 'subject':
                feedback_results.subject = attributevalues['val']
                continue

            iqv_key_value_set = IQVKeyValueSet()
            iqv_key_value_set.key = attributevalues['name']
            iqv_key_value_set.value = attributevalues['val']
            feedback_results.attribute_auxiliary_list.append(iqv_key_value_set)

    feedback_results.feedback_source = feedback_request['feedback_source']
    feedback_results.customer = feedback_request['customer']
    feedback_results.user_id = feedback_request['user_id']
    feedback_results.date_time_stamp = GetDateTimeString()
    feedback_results.protocol = feedback_request['protocol']
    feedback_results.country = feedback_request['country']
    feedback_results.site = feedback_request['site']
    feedback_results.document_class = feedback_request['document_class']
    feedback_results.document_date = feedback_request['document_date']
    feedback_results.expiry_date = feedback_request['expiration_date']
    feedback_results.document_classification = [feedback_request['document_classification']]
    feedback_results.name = feedback_request['name']
    feedback_results.language = feedback_request['language']
    feedback_results.document_rejected = str(feedback_request['document_rejected'])
    doc.IQVDocumentFeedbackResultsList.append(feedback_results)

    try:
        write_iqv_xml(feedback_output_path, doc)
        logger.info(f"Feedback values populated into feedback xml {feedback_output_path}")
        return feedback_output_path
    except Exception as e:
        raise FinalizationException(ErrorCodes.FEEDBACK_PROCESS_XML_WRITING_FAILURE, str(e))
