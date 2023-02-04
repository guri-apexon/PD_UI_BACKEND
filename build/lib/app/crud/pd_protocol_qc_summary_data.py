from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pd_protocol_qc_summary_data import PDProtocolQCSummaryData
from app.schemas.pd_protocol_qc_summary_data import ProtocolQCSummaryDataCreate, ProtocolQCSummaryDataUpdate


class CRUDProtocols(CRUDBase[PDProtocolQCSummaryData, ProtocolQCSummaryDataCreate, ProtocolQCSummaryDataUpdate]):
    def get_protocol_qc_summary_attributes(self, db: Session, id: Any) -> Optional[PDProtocolQCSummaryData]:
        """Retrieves a record based on primary key or id"""
        return db.query(PDProtocolQCSummaryData.aidocId,
                        PDProtocolQCSummaryData.amendmentNumber,
                        PDProtocolQCSummaryData.approvalDate,
                        PDProtocolQCSummaryData.indications,
                        PDProtocolQCSummaryData.moleculeDevice,
                        PDProtocolQCSummaryData.trialPhase,
                        PDProtocolQCSummaryData.protocolTitle,
                        PDProtocolQCSummaryData.sponsor,
                        PDProtocolQCSummaryData.versionNumber,
                        PDProtocolQCSummaryData.isAmendment,
                        PDProtocolQCSummaryData.protocolShortTitle
                        ).filter(PDProtocolQCSummaryData.aidocId == id, PDProtocolQCSummaryData.source == "QC",
                                 PDProtocolQCSummaryData.isActive == True).first()

    def create(self, db: Session, *, obj_in: ProtocolQCSummaryDataCreate) -> PDProtocolQCSummaryData:
        pass

    def update(
            self, db: Session, *, db_obj: PDProtocolQCSummaryData,
            obj_in: Union[ProtocolQCSummaryDataUpdate, Dict[str, Any]]
    ) -> PDProtocolQCSummaryData:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


pd_protocol_qc_summary_data = CRUDProtocols(PDProtocolQCSummaryData)
