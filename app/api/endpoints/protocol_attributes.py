import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.utilities.config import settings
from app.utilities import utils

logger = logging.getLogger(settings.LOGGER_NAME)

router = APIRouter()


@router.get("/")
def read_protocol_attributes(
        id: str,
        getQcInprogressAttr: bool = False,
        db: Session = Depends(deps.get_db)
) -> Any:
    """
        Retrieve Protocol Attributes and enrich with QC data (if available)
    """
    logger.debug(f"Reading Protocol attributes for the aidocId: {id}")
    pd_attributes_for_dashboard = {}
    try:
        attributes_from_protocol_metadata = crud.pd_protocol_metadata.get_protocol_attributes(db, id)
        if attributes_from_protocol_metadata is not None:
            approval_date = attributes_from_protocol_metadata.approvalDate
            pd_attributes_for_dashboard['id'] = attributes_from_protocol_metadata.id
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
            pd_attributes_for_dashboard['qcStatus'] = attributes_from_protocol_metadata.qcStatus
            pd_attributes_for_dashboard['uploadDate'] = attributes_from_protocol_metadata.uploadDate
            pd_attributes_for_dashboard['moleculeDevice'] = attributes_from_protocol_metadata.moleculeDevice
            pd_attributes_for_dashboard['phase'] = attributes_from_protocol_metadata.phase
            pd_attributes_for_dashboard['protocolTitle'] = attributes_from_protocol_metadata.protocolTitle
            pd_attributes_for_dashboard['amendmentNumber'] = None # Only present in QC record
            pd_attributes_for_dashboard['approvalDate'] = approval_date.strftime('%Y-%m-%d') if approval_date is not None else None
        else:
            logger.error(f'pd-ui-backend: No Protocol metadata found for the given aidocID')
            raise HTTPException(status_code=401, detail=f"No Protocol metadata found for the given aidocID")

        pd_attributes_for_dashboard = utils.update_qc_fields(pd_attributes_for_dashboard, get_qc_inprogress_attr_flg = getQcInprogressAttr, db = db)

        return pd_attributes_for_dashboard
    except Exception as ex:
        logger.exception(f"pd-ui-backend: Exception occured in reading protocol attributes for the aidocId: {id}")
        raise HTTPException(status_code=401, detail=f"Exception occurred in reading protocol attributes {str(ex)}")
