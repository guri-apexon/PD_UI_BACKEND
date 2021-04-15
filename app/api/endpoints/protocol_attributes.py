import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.utilities.config import settings

logger = logging.getLogger(settings.LOGGER_NAME)

router = APIRouter()


@router.get("/")
def read_protocol_attributes(
        db: Session = Depends(deps.get_db),
        id: str = "id",
) -> Any:
    """
    Retrieve Protocol Attributes.
    """
    logger.info(f"Reading Protocol attributes for the aidocId: {id}")
    pd_attributes_for_dashboard = {}
    try:
        attributes_from_protocol_metadata = crud.pd_protocol_metadata.get_protocol_attributes(db, id)
        if attributes_from_protocol_metadata is not None:
            pd_attributes_for_dashboard['aidocId'] = attributes_from_protocol_metadata.id
            pd_attributes_for_dashboard['amendment'] = attributes_from_protocol_metadata.amendment
            pd_attributes_for_dashboard[
                'completenessOfDigitization'] = attributes_from_protocol_metadata.completenessOfDigitization
            pd_attributes_for_dashboard[
                'digitizedConfidenceInterval'] = attributes_from_protocol_metadata.digitizedConfidenceInterval
            pd_attributes_for_dashboard['documentFilePath'] = attributes_from_protocol_metadata.documentFilePath
            pd_attributes_for_dashboard['documentStatus'] = attributes_from_protocol_metadata.documentStatus
            pd_attributes_for_dashboard['draftVersion'] = attributes_from_protocol_metadata.draftVersion
            pd_attributes_for_dashboard['errorCode'] = attributes_from_protocol_metadata.errorCode
            pd_attributes_for_dashboard['errorReason'] = attributes_from_protocol_metadata.errorReason
            pd_attributes_for_dashboard['fileName'] = attributes_from_protocol_metadata.fileName
            pd_attributes_for_dashboard['indication'] = attributes_from_protocol_metadata.indication
            pd_attributes_for_dashboard['sponsor'] = attributes_from_protocol_metadata.sponsor
            pd_attributes_for_dashboard['versionNumber'] = attributes_from_protocol_metadata.versionNumber
            pd_attributes_for_dashboard['percentComplete'] = attributes_from_protocol_metadata.percentComplete
            pd_attributes_for_dashboard['projectId'] = attributes_from_protocol_metadata.projectId
            pd_attributes_for_dashboard['protocol'] = attributes_from_protocol_metadata.protocol
            pd_attributes_for_dashboard['userId'] = attributes_from_protocol_metadata.userId
            pd_attributes_for_dashboard['status'] = attributes_from_protocol_metadata.status
            pd_attributes_for_dashboard['uploadDate'] = attributes_from_protocol_metadata.uploadDate
        else:
            logger.error(f'pd-ui-backend: No Protocol metadata found for the given aidocID')
            raise HTTPException(status_code=401, detail=f"No Protocol metadata found for the given aidocID")
        attributes_from_protocol_qc_summary_data = crud.pd_protocol_qc_summary_data.get_protocol_qc_summary_attributes(
            db, id)
        if attributes_from_protocol_qc_summary_data is not None:
            pd_attributes_for_dashboard['amendmentNumber'] = attributes_from_protocol_qc_summary_data.amendmentNumber
            pd_attributes_for_dashboard['approvalDate'] = attributes_from_protocol_qc_summary_data.approvalDate
            pd_attributes_for_dashboard['moleculeDevice'] = attributes_from_protocol_qc_summary_data.moleculeDevice
            pd_attributes_for_dashboard['phase'] = attributes_from_protocol_qc_summary_data.trialPhase
            pd_attributes_for_dashboard['protocolTitle'] = attributes_from_protocol_qc_summary_data.protocolTitle
            if attributes_from_protocol_metadata.percentComplete == "100" and \
                    attributes_from_protocol_metadata.status == "PROCESS_COMPLETED":
                pd_attributes_for_dashboard['indication'] = attributes_from_protocol_qc_summary_data.indications
                pd_attributes_for_dashboard['sponsor'] = attributes_from_protocol_qc_summary_data.sponsor
                pd_attributes_for_dashboard['versionNumber'] = attributes_from_protocol_qc_summary_data.versionNumber
        else:
            pd_attributes_for_dashboard['amendmentNumber'] = None
            pd_attributes_for_dashboard['approvalDate'] = None
            pd_attributes_for_dashboard['moleculeDevice'] = None
            pd_attributes_for_dashboard['phase'] = None
            pd_attributes_for_dashboard['protocolTitle'] = None
        return pd_attributes_for_dashboard
    except Exception as ex:
        logger.exception(f"pd-ui-backend: Exception occured in reading protocol attributes for the aidocId: {id}")
        raise HTTPException(status_code=401, detail=f"Exception occurred in reading protocol attributes {str(ex)}")
