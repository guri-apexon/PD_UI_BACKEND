from etmfa_finalization import Constants
from dataclasses import asdict
from etmfa_finalization.core.models import DocumentAttributes
from etmfa_finalization.core.models import ProcessingAttributes


class FinalizationRequestByFile:
    """ POCO message request for an initial request for the formatting microservice"""

    QUEUE_NAME = 'finalization_request'

    def __init__(self, filePath):
        """
        :filePath:  Fully-qualified path of the document to segment
        """
        self.filePath = filePath


class FinalizationComplete:

    QUEUE_NAME = 'finalization_complete'

    # def __init__(self, doc_attributes: DocumentAttributes, doc_metrics: ProcessingAttributes):
    #     self.__dict__.update(doc_attributes.flatten_dict())
    #     self.__dict__.update(asdict(doc_metrics))

    def __init__(self, doc_attributes: DocumentAttributes, doc_metrics: ProcessingAttributes):
        self.__dict__.update(doc_attributes.flatten_dict())
        self.__dict__.update(asdict(doc_metrics))

class FeedbackRequest:
    QUEUE_NAME = 'feedback_request'

    def __init__(self, input_path, id, feedback_source, customer, protocol, country, site,
                 document_class, document_date, document_classification, name,
                 language, document_rejected, attribute_auxillary_list):
        self.input_path = input_path
        self.id = id
        self.feedback_source = feedback_source
        self.customer = customer
        self.protocol = protocol
        self.country = country
        self.site = site
        self.document_class = document_class
        self.document_date = document_date
        self.document_classification = document_classification
        self.name = name
        self.language = language
        self.document_rejected = document_rejected
        self.attribute_auxillary_list = attribute_auxillary_list


class FeedbackComplete:
    QUEUE_NAME = 'feedback_complete'

    def __init__(self, id, fileName):
        self.id = id
        self.fileName = fileName


class Document_Processing_Error:
    QUEUE_NAME = 'documentprocessing_error'

    def __init__(self, id, error_code, error_message, error_message_details=None):
        self.service_name = Constants.MICROSERVICE_NAME
        self.id = id
        self.error_code = error_code
        self.error_message = error_message
        self.error_message_details = error_message_details if error_message_details else error_message
