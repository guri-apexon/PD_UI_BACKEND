from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app import crud, schemas, config
from app.api import deps
from app.api.endpoints import auth

router = APIRouter()

@router.get("/", response_model=List[schemas.ProtocolMetadataRelatedProtocols])
def read_related_protocols(
        db: Session = Depends(deps.get_db),
        protocol: str = "protocol",
        userId: str = "userId",
        _: str = Depends(auth.validate_user_token)
) -> Any:
    """
    Retrieve Protocol Attributes.
    """
    related_protocols = crud.pd_protocol_metadata.get_by_qc_approved_protocol(db, protocol)

    user_protocols = crud.pd_user_protocols.get_details_by_userId_protocol(db = db, userId = userId, protocol = protocol)
    user_role = 'secondary'
    if user_protocols:
        user_role = user_protocols[0].userRole

    user_ids = list({protocol.userId for protocol in related_protocols})
    user_details = crud.user.get_by_username_list(db, user_ids)
    user_details = {user_id: ' '.join([user_detail.first_name, user_detail.last_name]) for user_id, user_detail in user_details.items()}

    related_protocols_ret_val = list()
    for related_protocol in related_protocols:
        related_protocol_user_id = related_protocol.userId
        uploaded_by = ''
        if related_protocol_user_id:
            uploaded_by = user_details.get(config.REGEX_EMP_ID_ALPHA_REPLACE.sub('', related_protocol_user_id.lower()), '')

        approval_date = related_protocol.approvalDate
        if approval_date:
            approval_date = datetime.combine(approval_date, datetime.min.time())

        protocol_metadata_related_protocols = schemas.ProtocolMetadataRelatedProtocols(id = related_protocol.id,
                                                                                       userId = related_protocol.userId,
                                                                                       fileName = related_protocol.fileName,
                                                                                       documentFilePath = related_protocol.documentFilePath,
                                                                                       protocol = related_protocol.protocol,
                                                                                       versionNumber = related_protocol.versionNumber,
                                                                                       documentStatus = related_protocol.documentStatus,
                                                                                       status = related_protocol.status,
                                                                                       qcStatus = related_protocol.qcStatus,
                                                                                       uploadDate = related_protocol.uploadDate,
                                                                                       approvalDate = approval_date,
                                                                                       isActive = related_protocol.isActive,
                                                                                       uploadedBy = uploaded_by,
                                                                                       userRole = user_role)
        related_protocols_ret_val.append(protocol_metadata_related_protocols)

    return related_protocols_ret_val
