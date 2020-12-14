from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pd_user_protocol_documents import PD_User_Protocol_Documents
from app.schemas.pd_user_protocol_documents import UserProtocolDocumentsCreate, UserProtocolDocumentsUpdate


class CRUDUserProtocolDocuments(CRUDBase[PD_User_Protocol_Documents, UserProtocolDocumentsCreate,
                                         UserProtocolDocumentsUpdate]):

    def get_by_id(self, db: Session, *, user_protocol_document_id: int) -> Optional[PD_User_Protocol_Documents]:
        return db.query(PD_User_Protocol_Documents).filter(PD_User_Protocol_Documents.id ==
                                                           user_protocol_document_id).first()

    def create(self, db: Session, *, obj_in: UserProtocolDocumentsCreate) -> PD_User_Protocol_Documents:
        db_obj = PD_User_Protocol_Documents(id=obj_in.id,
                                            userId=obj_in.userId,
                                            fileName=obj_in.fileName,
                                            filePath=obj_in.filePath,
                                            Protocol=obj_in.Protocol,
                                            ProtocolName=obj_in.ProtocolName,
                                            ProjectId=obj_in.ProjectId,
                                            Sponser=obj_in.Sponser,
                                            Indication=obj_in.Indication,
                                            Molecule=obj_in.Molecule,
                                            Amendment=obj_in.Amendment,
                                            VersionNumber=obj_in.VersionNumber,
                                            DocumentStatus=obj_in.DocumentStatus,
                                            DraftVersion=obj_in.DraftVersion,
                                            errorCode=obj_in.errorCode,
                                            errorReason=obj_in.errorReason,
                                            Status=obj_in.Status,
                                            phase=obj_in.phase,
                                            DigitizedConfidenceInterval=obj_in.DigitizedConfidenceInterval,
                                            CompletenessOfDigitization=obj_in.CompletenessOfDigitization,
                                            protocolTitle=obj_in.protocolTitle,
                                            studyStatus=obj_in.studyStatus,
                                            sourceSystem=obj_in.sourceSystem,
                                            environment=obj_in.environment,
                                            uploadDate=obj_in.uploadDate,
                                            timeCreated=obj_in.timeCreated,
                                            timeUpdated=obj_in.timeUpdated,
                                            userCreated=obj_in.userCreated,
                                            userModified=obj_in.userModified,
                                            ApprovalDate=obj_in.ApprovalDate,
                                            isActive=obj_in.isActive,
                                            iqvxmlpath=obj_in.iqvxmlpath,
                                            NctId=obj_in.NctId, )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: PD_User_Protocol_Documents, obj_in: Union[UserProtocolDocumentsUpdate,
                                                                                    Dict[str, Any]]
    ) -> PD_User_Protocol_Documents:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


pd_user_protocol_document = CRUDUserProtocolDocuments(PD_User_Protocol_Documents)
