from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.api.endpoints import auth

router = APIRouter()

@router.get("/", response_model=List[schemas.ProtocolMetadataUploadUser])
def read_related_protocols(
        db: Session = Depends(deps.get_db),
        protocol: str = "protocol",
        userId: str = "userId",
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Retrieve Protocol Attributes.
    """
    related_protocols = crud.pd_protocol_metadata.get_by_protocol(db, protocol)

    user_protocols = crud.pd_user_protocols.get_details_by_userId_protocol(db = db, userId = userId, protocol = protocol)
    userRole = 'secondary'
    if user_protocols:
        userRole = user_protocols[0].userRole


    user_ids = list({protocol.userId for protocol in related_protocols})
    user_details = crud.user.get_by_username_list(db, user_ids)
    user_details = {user_detail.username.lower(): ' '.join([user_detail.first_name, user_detail.last_name]) for
                    user_detail in user_details}

    related_protocols_ret_val = list()
    for related_protocol in related_protocols:
        related_protocol_user_id = related_protocol.userId
        uploaded_by = ''
        if related_protocol_user_id:
            if related_protocol_user_id.lower().startswith(('q', 'u', 's')):
                uploaded_by = user_details.get(related_protocol_user_id.lower().lower(), '')
            else:
                related_protocol_q_user_id = 'q' + related_protocol_user_id.lower()
                related_protocol_u_user_id = 'u' + related_protocol_user_id.lower()
                related_protocol_s_user_id = 's' + related_protocol_user_id.lower()
                uploaded_by = ''
                if related_protocol_q_user_id in user_details:
                    uploaded_by = user_details.get(related_protocol_q_user_id, '')
                elif related_protocol_u_user_id in user_details:
                    uploaded_by = user_details.get(related_protocol_u_user_id, '')
                elif related_protocol_s_user_id in user_details:
                    uploaded_by = user_details.get(related_protocol_s_user_id, '')

        protocol_metadata_upload_user = schemas.ProtocolMetadataUploadUser(id = related_protocol.id,
                                                                           userId = related_protocol.userId,
                                                                           fileName = related_protocol.fileName,
                                                                           documentFilePath = related_protocol.documentFilePath,
                                                                           protocol = related_protocol.protocol,
                                                                           projectId = related_protocol.projectId,
                                                                           sponsor = related_protocol.sponsor,
                                                                           indication = related_protocol.indication,
                                                                           moleculeDevice = related_protocol.moleculeDevice,
                                                                           amendment = related_protocol.amendment,
                                                                           isProcessing = related_protocol.isProcessing,
                                                                           percentComplete = related_protocol.percentComplete,
                                                                           compareStatus = related_protocol.compareStatus,
                                                                           iqvXmlPathProc = related_protocol.iqvXmlPathProc,
                                                                           iqvXmlPathComp = related_protocol.iqvXmlPathComp,
                                                                           shortTitle = related_protocol.shortTitle,
                                                                           versionNumber = related_protocol.versionNumber,
                                                                           documentStatus = related_protocol.documentStatus,
                                                                           draftVersion = related_protocol.draftVersion,
                                                                           errorCode = related_protocol.errorCode,
                                                                           errorReason = related_protocol.errorReason,
                                                                           status = related_protocol.status,
                                                                           qcStatus = related_protocol.qcStatus,
                                                                           phase = related_protocol.phase,
                                                                           digitizedConfidenceInterval = related_protocol.digitizedConfidenceInterval,
                                                                           completenessOfDigitization = related_protocol.completenessOfDigitization,
                                                                           protocolTitle = related_protocol.protocolTitle,
                                                                           studyStatus = related_protocol.studyStatus,
                                                                           sourceSystem = related_protocol.sourceSystem,
                                                                           environment = related_protocol.environment,
                                                                           uploadDate = related_protocol.uploadDate,
                                                                           timeCreated = related_protocol.timeCreated,
                                                                           lastUpdated = related_protocol.lastUpdated,
                                                                           userCreated = related_protocol.userCreated,
                                                                           userUpdated = related_protocol.userUpdated,
                                                                           approvalDate = related_protocol.approvalDate,
                                                                           isActive = related_protocol.isActive,
                                                                           nctId = related_protocol.nctId,
                                                                           uploadedBy = uploaded_by,
                                                                           userRole = userRole)
        related_protocols_ret_val.append(protocol_metadata_upload_user)

    return related_protocols_ret_val
