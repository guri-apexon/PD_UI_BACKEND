from typing import Any, Dict, Optional, Union, Tuple

from elasticsearch import Elasticsearch
from fastapi import HTTPException
from sqlalchemy import or_, and_, case, func, literal
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app import crud
from app import config
from app.crud.base import CRUDBase
from app.models.pd_protocol_data import PD_Protocol_Data
from app.models.pd_protocol_metadata import PD_Protocol_Metadata
from app.models.pd_user_protocols import PD_User_Protocols
from app.models.pd_protocol_qc_summary_data import PDProtocolQCSummaryData
from app.schemas.pd_protocol_metadata import ProtocolMetadataCreate, ProtocolMetadataUpdate
from app.utilities.config import settings
from datetime import datetime


def update_elstic(es_dict, update_id):
    try:
        elasticsearches = Elasticsearch([{'host': settings.ELASTIC_HOST, 'port': settings.ELASTIC_PORT}])
        elasticsearches.update(index=settings.ELASTIC_INDEX, body={'doc': es_dict}, id=update_id)
        res = True
    except Exception as e:
        res = False

    elasticsearches.close()
    return (res)


class CRUDProtocolMetadata(CRUDBase[PD_Protocol_Metadata, ProtocolMetadataCreate,
                                    ProtocolMetadataUpdate]):

    def get_by_id(self, db: Session, *, id: int) -> Optional[PD_Protocol_Metadata]:
        return db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == id).first()

    def get(self, db: Session, id: Any) -> Optional[PD_Protocol_Metadata]:
        """Retrieves a record based on primary key or id"""
        return db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == id,
                                                     PD_Protocol_Metadata.isActive == True).first()

    def get_protocol_attributes(self, db: Session, id: Any) -> Optional[PD_Protocol_Metadata]:
        """Retrieves a record based on primary key or id"""
        return db.query(PD_Protocol_Metadata.id,
                        PD_Protocol_Metadata.amendment,
                        PD_Protocol_Metadata.completenessOfDigitization,
                        PD_Protocol_Metadata.digitizedConfidenceInterval,
                        PD_Protocol_Metadata.documentFilePath,
                        PD_Protocol_Metadata.documentStatus,
                        PD_Protocol_Metadata.draftVersion,
                        PD_Protocol_Metadata.errorCode,
                        PD_Protocol_Metadata.errorReason,
                        PD_Protocol_Metadata.fileName,
                        PD_Protocol_Metadata.indication,
                        PD_Protocol_Metadata.percentComplete,
                        PD_Protocol_Metadata.projectId,
                        PD_Protocol_Metadata.protocol,
                        PD_Protocol_Metadata.sponsor,
                        PD_Protocol_Metadata.status,
                        PD_Protocol_Metadata.qcStatus,
                        PD_Protocol_Metadata.uploadDate,
                        PD_Protocol_Metadata.userId,
                        PD_Protocol_Metadata.versionNumber,
                        PD_Protocol_Metadata.protocolTitle,
                        PD_Protocol_Metadata.moleculeDevice,
                        PD_Protocol_Metadata.phase,
                        PD_Protocol_Metadata.approvalDate
                        ).filter(PD_Protocol_Metadata.id == id,
                                                                PD_Protocol_Metadata.isActive == True).first()

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
                                      qcStatus=obj_in.qcStatus,
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

    def create_soft_delete(self, db: Session, *, obj_in: ProtocolMetadataCreate) -> PD_Protocol_Metadata:
        db_obj = PD_Protocol_Metadata(id=obj_in.id,
                                      userId=obj_in.userId,
                                      protocol=obj_in.protocol,
                                      projectId=obj_in.projectId,
                                      sponsor=obj_in.sponsor, )
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as ex:
            db.rollback()
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
        return db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.protocol == protocol,
                                                     PD_Protocol_Metadata.isActive == True,
                                                     PD_Protocol_Metadata.status == config.DIGITIZATION_COMPLETED_STATUS).all()

    # used in comparison of associated documents by protocol  
    def associated_docs_by_protocol(self, db: Session, protocol: str) -> Optional[PD_Protocol_Metadata]:
        return db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.protocol == protocol,
                                                     PD_Protocol_Metadata.isActive == True).all()

    async def get_by_doc_id(self, db: Session, id: Any, user_id: str) -> Optional[list]:
        """Retrieves a record based on primary key or id"""
        protocol_metadata = []
        protocol_metadata_first = db.query(PD_Protocol_Metadata, PD_User_Protocols.redactProfile.label("redactProfile"))\
            .join(PD_User_Protocols, and_(user_id == PD_User_Protocols.userId,
                                          PD_Protocol_Metadata.protocol == PD_User_Protocols.protocol), isouter=True)\
            .filter(PD_Protocol_Metadata.id == id, PD_Protocol_Metadata.isActive == True).first()

        if protocol_metadata_first:
            protocol_metadata = [{**protocol_metadata_first[0].as_dict(),
                                  **{"redactProfile": protocol_metadata_first[1]}}]
        return protocol_metadata

    def get_by_qc_approved_protocol(self, db: Session, protocol: str):
        """Retrieves protocol metadata for given protocol number and approval date from pd_protocol_qc_summary_data if QC Completed"""

        resource = db.query(PD_Protocol_Metadata.id,
                            PD_Protocol_Metadata.userId,
                            PD_Protocol_Metadata.fileName,
                            PD_Protocol_Metadata.documentFilePath,
                            PD_Protocol_Metadata.protocol,
                            PD_Protocol_Metadata.versionNumber,
                            PD_Protocol_Metadata.documentStatus,
                            PD_Protocol_Metadata.status,
                            PD_Protocol_Metadata.qcStatus,
                            PD_Protocol_Metadata.uploadDate,
                            PD_Protocol_Metadata.isActive,
                            PDProtocolQCSummaryData.source,
                            case([(PD_Protocol_Metadata.qcStatus == config.QcStatus.COMPLETED.value,
                                   PDProtocolQCSummaryData.approvalDate)
                                  ],
                                 else_= PD_Protocol_Metadata.approvalDate).label('approvalDate')
                            ).join(PDProtocolQCSummaryData,
                                   and_(PD_Protocol_Metadata.id == PDProtocolQCSummaryData.aidocId,
                                        PDProtocolQCSummaryData.source == config.QC,),
                                   isouter = True).filter(PD_Protocol_Metadata.protocol == protocol,
                                                          PD_Protocol_Metadata.isActive == True,
                                                          PD_Protocol_Metadata.status == config.DIGITIZATION_COMPLETED_STATUS
                                                          ).all()
        return resource

    async def get_metadata_by_userId(self, db: Session, userId: str) -> Optional[list]:
        """Retrieves all protocol metadata along with follow flag and user roles"""
        all_protocol_metadata = \
            db.query(PD_Protocol_Metadata, 
                        case(
                                [(PD_Protocol_Metadata.userId == userId, True)
                                ], 
                                else_ = False).label('uploaded_by_user_flg'),
                        case(
                                [(and_(PD_User_Protocols.userId == userId, PD_User_Protocols.userRole == config.UserRole.PRIMARY.value), True)
                                ], 
                                else_ = False).label('primary_role_flg'),                                          
                        func.row_number().over(
                            partition_by = PD_Protocol_Metadata.id,
                            order_by = (PD_User_Protocols.userRole.asc(), PD_User_Protocols.follow.desc())
                                            ).label('rank'),
                        PD_User_Protocols.follow.label('follow_flg'),
                        PD_User_Protocols.redactProfile.label('redactProfile')
                    ).join(PD_User_Protocols, PD_Protocol_Metadata.protocol == PD_User_Protocols.protocol , isouter = True
                    ).filter(and_(or_(PD_Protocol_Metadata.userId == userId, PD_User_Protocols.userId == userId), 
                                PD_Protocol_Metadata.isActive == True)).all()

        protocol_metadata = [{**row.PD_Protocol_Metadata.as_dict(), **{'userUploadedFlag': row.uploaded_by_user_flg if row.uploaded_by_user_flg is not None else False, \
                                                                       'userPrimaryRoleFlag': row.primary_role_flg if row.primary_role_flg is not None else False, \
                                                                       'userFollowingFlag': row.follow_flg if row.follow_flg is not None else False, \
                                                                       'redactProfile': row.redactProfile}} \
                                                                             for row in all_protocol_metadata \
                                        if row.rank == 1 and (row.uploaded_by_user_flg == True or row.primary_role_flg == True or row.follow_flg == True)]

        return protocol_metadata

    async def get_qc_protocols(self, db: Session, status: str) -> Optional[list]:
        """Retrieves a record based on user id"""
        all_protocol_metadata = db.query(PD_Protocol_Metadata)\
                                        .filter(PD_Protocol_Metadata.qcStatus == status,
                                            PD_Protocol_Metadata.status == config.DIGITIZATION_COMPLETED_STATUS,
                                            PD_Protocol_Metadata.isActive == True)\
                                        .all()

        protocol_metadata = [row.as_dict()  for row in all_protocol_metadata]
        return protocol_metadata

    async def get_qc_status(self, db: Session, doc_id: str = None) -> Optional[list]:
        """
        Retrieves qcStatus of all successfully digitized protocols
        Optional: Extract specific doc_id
        """
        protocol_metadata = []
        if doc_id is not None:
            protocol_metadata_first = db.query(PD_Protocol_Metadata.id, PD_Protocol_Metadata.qcStatus)\
                                        .filter(PD_Protocol_Metadata.status == config.DIGITIZATION_COMPLETED_STATUS,
                                            PD_Protocol_Metadata.isActive == True, PD_Protocol_Metadata.id == doc_id)\
                                        .first()
            if protocol_metadata_first:
                protocol_metadata = [protocol_metadata_first._asdict()]
        else:
            all_protocol_metadata = db.query(PD_Protocol_Metadata.id, PD_Protocol_Metadata.qcStatus)\
                                        .filter(PD_Protocol_Metadata.status == config.DIGITIZATION_COMPLETED_STATUS,
                                            PD_Protocol_Metadata.isActive == True)\
                                        .all()

            protocol_metadata = [row._asdict()  for row in all_protocol_metadata]
        return protocol_metadata

    def activate_protocol(self, db: Session, aidoc_id: str) -> Any:
        """Retrieves a record based on user id"""
        is_protocol_active = db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == aidoc_id,
                                                                   PD_Protocol_Metadata.isActive == 1).first()
        if is_protocol_active:
            raise HTTPException(status_code=200, detail="Protocol is already Active")

        protocol = db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == aidoc_id).first()
        if not protocol:
            raise HTTPException(status_code=401, detail="Record not found for the given aidoc id")
        else:
            try:
                protocol.isActive = 1
                db.commit()
                db.refresh(protocol)
                return True
            except Exception as ex:
                db.rollback()
                raise HTTPException(status_code=401,
                                    detail=f"Exception occured during updating isActive in DB{str(ex)}")

    async def change_qc_status(self, db: Session, doc_id: str, target_status: str, current_timestamp = datetime.utcnow()) -> Tuple[bool, str]:
        """
        Changes QC Activity status on the given doc_id
        """
        prot_metadata_doc = db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == doc_id, PD_Protocol_Metadata.isActive == True).first()

        if not prot_metadata_doc:
            return False, "No protocol document found for the requested doc id"

        current_qc_status = prot_metadata_doc.qcStatus
        if current_qc_status == target_status:
            return True, f"Protocol's qcStatus is already in {target_status}"

        try:
            prot_metadata_doc.qcStatus = target_status
            prot_metadata_doc.lastUpdated = current_timestamp
            db.commit()
            return True, f"Successfully changed qcStatus from {current_qc_status} to {target_status}"
        except Exception as ex:
            db.rollback()
            return False, f"Exception occured during updating {current_qc_status} to {target_status} in DB [{str(ex)}]"

    def get_latest_protocol(self, db: Session, protocol: str, versionNumber: str) -> Optional[PD_Protocol_Metadata]:
        """Retrieves a record based on protocol and versionNumber"""
        if versionNumber is None:
            return db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.isActive == True,
                                                         PD_Protocol_Metadata.status == "PROCESS_COMPLETED",
                                                         PD_Protocol_Metadata.protocol == protocol).order_by(
                PD_Protocol_Metadata.versionNumber.desc()).first()
        else:
            return db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.isActive == True,
                                                         PD_Protocol_Metadata.status == "PROCESS_COMPLETED",
                                                         PD_Protocol_Metadata.protocol == protocol,

                                                         PD_Protocol_Metadata.versionNumber >= versionNumber).order_by(
                PD_Protocol_Metadata.versionNumber.desc()).first()

    def get_metadata_by_filter(self, db: Session, filter) -> Optional[PD_Protocol_Metadata]:
        """Retrieves a record based on user id"""
        if filter['protocol'] == None and filter['projectId'] == None:
            raise HTTPException(status_code=404,
                                detail="Both Protocol Number and Project Id can't be None pass atleast one")
        res = db.query(PD_Protocol_Metadata)
        delFilter = ''
        # Filter String is formed by query filtered passed with Not None values
        for key, filt in filter.items():
            if filt is not None:
                delFilter = ("{}='{}' and {}".format(key, filt, delFilter))
        return (res.filter(text(delFilter[:-4])).all())

    def execute_metadata_by_deleteCondition(self, db: Session, records: Any, is_Active: bool) -> Optional[
        PD_Protocol_Metadata]:
        """Retrieves a record based on user id"""
        for record in records:
            pd_data = crud.pd_protocol_data.get_by_id(db, id=record.id)
            record.isActive = is_Active
            # pd_data.isActive=is_Active
            try:
                db.commit()
                elastic_status = update_elstic(es_dict={'is_active': (1 if is_Active else 0)
                                                        }, update_id=record.id)
                if elastic_status == False:
                    raise Exception
            except Exception as ex:
                db.rollback()

        return records

    def get_latest_approved_document(self, db: Session, protocol: str) -> Optional[PD_Protocol_Metadata]:
        return db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.protocol == protocol).filter(
            PD_Protocol_Metadata.documentStatus == 'final').order_by(PD_Protocol_Metadata.uploadDate.desc()).first()


pd_protocol_metadata = CRUDProtocolMetadata(PD_Protocol_Metadata)
