from typing import Any, Dict, Optional, Union
import requests
import json
import pandas as pd

from sqlalchemy.orm import Session

from fastapi import HTTPException

from app.crud.base import CRUDBase
from app.models.pd_protocol_data import PD_Protocol_Data
from app.schemas.pd_protocol_data import ProtocolDataCreate, ProtocolDataUpdate, ProtocolData
from app.utilities.file_utils import write_data_to_json, write_data_to_xlsx


class CRUDProtocolData(CRUDBase[PD_Protocol_Data, ProtocolDataCreate, ProtocolDataUpdate]):
    def get_by_id(self, db: Session, *, id: Any) -> Optional[PD_Protocol_Data]:
        return db.query(PD_Protocol_Data).filter(PD_Protocol_Data.id == id).first()

    def get(self, db: Session, id: Any) -> Optional[PD_Protocol_Data]:
        """Retrieves a record based on primary key or id"""
        return db.query(PD_Protocol_Data).filter(PD_Protocol_Data.id == id, PD_Protocol_Data.isActive == True).first()

    def create(self, db: Session, *, obj_in: ProtocolDataCreate) -> PD_Protocol_Data:
        db_obj = PD_Protocol_Data(id=obj_in.id,
                                  userId=obj_in.userId,
                                  fileName=obj_in.fileName,
                                  documentFilePath=obj_in.documentFilePath,
                                  iqvdataToc=obj_in.iqvdataToc,
                                  iqvdataSoa=obj_in.iqvdataSoa,
                                  iqvdataSoaStd=obj_in.iqvdataSoaStd,
                                  iqvdataSummary=obj_in.iqvdataSummary,
                                  iqvdata=obj_in.iqvdata, )
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as ex:
            db.rollback()
        return db_obj

    def update(
            self, db: Session, *, db_obj: PD_Protocol_Data, obj_in: Union[ProtocolDataUpdate, Dict[str, Any]]
    ) -> PD_Protocol_Data:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


    def generate_iqvdata_json_file(self, db: Session, aidoc_id: str):
        URL = "http://ca2spdml06d:8000/api/protocol_data/"
        PARAMS = {'id': aidoc_id}
        r = requests.get(url=URL, params=PARAMS)
        data = r.json()
        json_path = write_data_to_json(aidoc_id, data)
        return json_path

    def generate_iqvdata_xlsx_file(self, db: Session, aidoc_id: str):
        URL = "http://ca2spdml06d:8000/api/protocol_data/"
        PARAMS = {'id': aidoc_id}
        r = requests.get(url=URL, params=PARAMS)
        data = r.json()
        xlsx_path = write_data_to_xlsx(aidoc_id, data)
        return xlsx_path

    def qc_approve(self, db: Session, aidoc_id: str) -> Any:
        """QC approves for the protocol with given qid"""
        is_qc_protocol_active = db.query(PD_Protocol_Data).filter(PD_Protocol_Data.id == aidoc_id,
                                                                  PD_Protocol_Data.isActive == 1).first()
        if is_qc_protocol_active:
            raise HTTPException(status_code=200, detail="Protocol is already Active")

        qc_protocol = db.query(PD_Protocol_Data).filter(PD_Protocol_Data.id == aidoc_id).first()
        if not qc_protocol:
            raise HTTPException(status_code=401, detail="Record not found for the given aidoc id")
        else:
            try:
                qc_protocol.isActive = 1
                db.commit()
                db.refresh(qc_protocol)
                return True
            except Exception as ex:
                db.rollback()
                raise HTTPException(status_code=401,
                                    detail=f"Exception occured during updating isActive in DB{str(ex)}")


pd_protocol_data = CRUDProtocolData(PD_Protocol_Data)
