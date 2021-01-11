from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pd_protocol_metadata import PD_Protocol_Metadata
from app.schemas.pd_protocol_metadata import ProtocolMetadataCreate, ProtocolMetadataUpdate


class CRUDProtocolMetadata(CRUDBase[PD_Protocol_Metadata, ProtocolMetadataCreate,
                                         ProtocolMetadataUpdate]):

    def get_by_id(self, db: Session, *, id: int) -> Optional[PD_Protocol_Metadata]:
        return db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == id).first()

    def create(self, db: Session, *, obj_in: ProtocolMetadataCreate) -> PD_Protocol_Metadata:
        db_obj = PD_Protocol_Metadata(id=obj_in.id,
                                            userId=obj_in.userId,
                                            fileName=obj_in.fileName,
                                            documentFilePath=obj_in.documentFilePath,
                                            protocol=obj_in.protocol,
                                            projectId=obj_in.projectId,
                                            sponsor=obj_in.sponsor,
                                            indication=obj_in.indication,
                                            isProcessing=obj_in.isProcessing,
                                            moleculeDevice=obj_in.moleculeDevice,
                                            amendment=obj_in.amendment,
                                            percentComplete=obj_in.percentComplete,
                                            versionNumber=obj_in.versionNumber,
                                            documentStatus=obj_in.documentStatus,
                                            draftVersion=obj_in.draftVersion,
                                            errorCode=obj_in.errorCode,
                                            errorReason=obj_in.errorReason,
                                            status=obj_in.status,
                                            phase=obj_in.phase,
                                            digitizedConfidenceInterval=obj_in.digitizedConfidenceInterval,
                                            completenessOfDigitization=obj_in.completenessOfDigitization,
                                            protocolTitle=obj_in.protocolTitle,
                                            shortTitle=obj_in.shortTitle,                           
                                            studyStatus=obj_in.studyStatus,
                                            sourceSystem=obj_in.sourceSystem,
                                            environment=obj_in.environment,
                                            uploadDate=obj_in.uploadDate,
                                            timeCreated=obj_in.timeCreated,
                                            lastUpdated=obj_in.lastUpdated,
                                            userCreated=obj_in.userCreated,
                                            userUpdated=obj_in.userUpdated,
                                            approvalDate=obj_in.approvalDate,
                                            isActive=obj_in.isActive,
                                            compareStatus=obj_in.compareStatus,
                                            iqvXmlPathProc=obj_in.iqvXmlPathProc,
                                            iqvXmlPathComp=obj_in.iqvXmlPathComp,
                                            nctId=obj_in.nctId, )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: PD_Protocol_Metadata, obj_in: Union[ProtocolMetadataUpdate,
                                                                                    Dict[str, Any]]
    ) -> PD_Protocol_Metadata:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)
    
    def get_by_protocol(self, db: Session, protocol: str) -> Optional[PD_Protocol_Metadata]:
        return db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.protocol == protocol).all()
    
    def get_metadata_by_userId(self, db: Session, userId: str) -> Optional[PD_Protocol_Metadata]:
        """Retrieves a record based on user id"""
        return db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.userId == userId, PD_Protocol_Metadata.isActive == True).order_by(PD_Protocol_Metadata.timeCreated.desc()).all()

    def get_latest_protocol(self, db: Session, protocol: str, versionNumber:str) -> Optional[PD_Protocol_Metadata]:
        """Retrieves a record based on protocol and versionNumber"""
        if versionNumber is None:
            return db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.isActive == True, 
                                                        PD_Protocol_Metadata.status == "PROCESS_COMPLETED", 
                                                        PD_Protocol_Metadata.protocol == protocol).order_by(PD_Protocol_Metadata.versionNumber.desc()).first()
        else:
            return db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.isActive == True, 
                                                        PD_Protocol_Metadata.status == "PROCESS_COMPLETED", 
                                                        PD_Protocol_Metadata.protocol == protocol,
                                                        PD_Protocol_Metadata.versionNumber >= versionNumber).order_by(PD_Protocol_Metadata.versionNumber.desc()).first()


pd_protocol_metadata = CRUDProtocolMetadata(PD_Protocol_Metadata)
