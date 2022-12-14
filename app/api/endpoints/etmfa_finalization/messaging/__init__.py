# import os
# import threading
#
# from kombu import Connection
#
# from etmfa_core.aidoc.io import read_iqv_xml
# from etmfa_core.aidoc.io import write_iqv_xml
# from etmfa_core.aidoc.IQVDocumentFunctions import SetWorkflowSubProcess
# from etmfa_core.aidoc.models.IQVUtilities import GetDateTimeString
# from etmfa_finalization import Constants, Globals
# from etmfa_finalization.core.iqv_feedback_loop import populate_feedback_into_xml
# from etmfa_finalization.messaging.messagelistener import MessageListener
# from etmfa_finalization.messaging.messagepublisher import MessagePublisher
# from iqv_finalization_error import ErrorCodes, FinalizationException
# from etmfa_finalization.messaging.prepare_update_data import PrepareUpdateData
# from .models.finalization_request import (FeedbackComplete, FeedbackRequest,
#                                           FinalizationComplete,
#                                           FinalizationRequestByFile)
#
#
# import etmfa_finalization.messaging.prepare_update_data
# import json
# import logging
#
# logger = logging.getLogger(Constants.MICROSERVICE_NAME)
#
#
# def _msg_listening_worker(app, listener):
#     with app.app_context():
#         listener.run()
#
#
# def initialize_msg_listeners(app, connection_str, exchange_name, logger):
#     """
#     Run Message Listeners on a daemon thread.
#     """
#     with Connection(connection_str) as conn:
#         consumer = MessageListener(conn, connection_str, exchange_name, logger=logger)
#         consumer = _build_queue_callbacks(consumer)
#
#         daemon_handle = threading.Thread(
#             name='msg_listener_daemon',
#             target=_msg_listening_worker,
#             args=(app, consumer,))
#
#         daemon_handle.setDaemon(True)
#         daemon_handle.start()
#         logger.info("Consuming queues...")
#
#     return daemon_handle
#
#
# def _build_queue_callbacks(queue_worker):
#     queue_worker.add_listener(FinalizationRequestByFile.QUEUE_NAME, _on_finalization_receipt)
#     return queue_worker
#
#
# def _on_feedback_receipt(feedback_req_dict: dict, message_publisher: MessagePublisher):
#     feedback_xml_path = populate_feedback_into_xml(feedback_req_dict)
#
#     msg = FeedbackComplete(feedback_req_dict["id"], feedback_xml_path)
#     message_publisher.send_obj(msg)
#
#
# def _on_finalization_receipt(finalization_req_dict: dict, message_publisher: MessagePublisher):
#
#     """Called when finalization request RabbitMQ message is received.
#
#     Function extracts individual attributes from IQVIA XML.
#     These are transformed accordingly and in the end
#     passed to management service via RabbitMQ as well as
#     feedback results for AI pipeline are appended to IQVIA XML.
#
#     Args:
#         finalization_req_dict (dic): dictionary with doc id and path to iqvia xml
#         message_publisher: RabbitMQ publisher obj.
#     """
#     input_path = finalization_req_dict["IQVXMLPath"]
#     FeedbackRunId = finalization_req_dict.get("FeedbackRunId", 0)
#     OutputFilePrefix = finalization_req_dict.get('OutputFilePrefix', '')
#
#     try:
#         logger.info(f"Reading iqv_xml [{GetDateTimeString()}]: {input_path}")
#         iqvia_doc = read_iqv_xml(input_path)
#         logger.info(f"Completed reading iqv_xml [{GetDateTimeString()}]: {input_path}")
#     except Exception as e:
#         raise FinalizationException(ErrorCodes.XML_READING_FAILURE, str(e))
#
#     filename = os.path.basename(input_path)
#     dir_name = os.path.dirname(input_path)
#     output_iqvia_doc_path = os.path.join(dir_name, f"{OutputFilePrefix}FIN_" + filename)
#     finalization_req_dict["IQVXMLPath"] = output_iqvia_doc_path
#     finalized_iqvxml=PrepareUpdateData(iqvia_doc, FeedbackRunId)
#     finalization_req_dict["db_data"], updated_iqv_document = finalized_iqvxml.prepare_msg()
#
#     logger.info(f"Writing update_iqv_document [{GetDateTimeString()}]: {output_iqvia_doc_path}")
#
#     SetWorkflowSubProcess(updated_iqv_document,
#                           subprocess=Constants.MICROSERVICE_NAME,
#                           required=True,
#                           startTime=GetDateTimeString(),
#                           machineName=Globals.HOST_NAME,
#                           version=Globals.VERSION)
#
#     write_iqv_xml(output_iqvia_doc_path, updated_iqv_document)
#     logger.info(f"Completed writing update_iqv_document [{GetDateTimeString()}]: {output_iqvia_doc_path}")
#
#     message_publisher.send_str(json.dumps(finalization_req_dict), FinalizationComplete.QUEUE_NAME)
