from app import config, crud
from sqlalchemy.orm import Session
import requests
from app.utilities.config import settings
import logging

logger = logging.getLogger(settings.LOGGER_NAME)

async def update_qc_fields(pd_attributes_for_dashboard: dict, db: Session, get_qc_inprogress_attr_flg: bool = False) -> dict():
    """
        Enrich the input dictionary with QC'd data only if the QC is completed (OR) override flag 'get_qc_inprogress_attr_flg' is set
    """
    attributes_from_protocol_qc_summary_data = None
    aidoc_id = pd_attributes_for_dashboard['id']
    pd_attributes_for_dashboard['shortTitle'] = '' # Not used and not configured for partial redaction

    if  pd_attributes_for_dashboard['qcStatus'] == config.QcStatus.COMPLETED.value or get_qc_inprogress_attr_flg:          
        attributes_from_protocol_qc_summary_data = crud.pd_protocol_qc_summary_data.get_protocol_qc_summary_attributes(db, aidoc_id)

    if attributes_from_protocol_qc_summary_data is not None:
        pd_attributes_for_dashboard['amendment'] = attributes_from_protocol_qc_summary_data.isAmendment
        pd_attributes_for_dashboard['amendmentNumber'] = attributes_from_protocol_qc_summary_data.amendmentNumber
        pd_attributes_for_dashboard['approvalDate'] = attributes_from_protocol_qc_summary_data.approvalDate
        pd_attributes_for_dashboard['indication'] = attributes_from_protocol_qc_summary_data.indications
        pd_attributes_for_dashboard['sponsor'] = attributes_from_protocol_qc_summary_data.sponsor
        pd_attributes_for_dashboard['versionNumber'] = attributes_from_protocol_qc_summary_data.versionNumber
        pd_attributes_for_dashboard['moleculeDevice'] = attributes_from_protocol_qc_summary_data.moleculeDevice
        pd_attributes_for_dashboard['phase'] = attributes_from_protocol_qc_summary_data.trialPhase
        pd_attributes_for_dashboard['protocolTitle'] = attributes_from_protocol_qc_summary_data.protocolTitle

    return pd_attributes_for_dashboard


def notification_service(doc_id: str, event: str, send_mail: bool, user_id: str = '') -> bool:
    PARAMS = {"doc_id": doc_id, "event": event, "send_mail":send_mail, "user_id":user_id}
    response_qc_mail = requests.get(url=settings.MANAGEMENT_SERVICE_URL+"notifications/send/email", params=PARAMS, headers=settings.MGMT_CRED_HEADERS)
    logger.info(f"for doc id {doc_id} event {event} records create")
    return True