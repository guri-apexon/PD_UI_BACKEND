import json
from typing import Any, Dict, Optional, Union

import pandas as pd
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pd_protocol_qcdata import PD_Protocol_QCData
from app.schemas.pd_protocol_qcdata import ProtocolQCDataCreate, ProtocolQCDataUpdate


class CRUDProtocolQCData(CRUDBase[PD_Protocol_QCData, ProtocolQCDataCreate, ProtocolQCDataUpdate]):
    def get_by_id(self, db: Session, id: Any) -> Optional[PD_Protocol_QCData]:
        return db.query(PD_Protocol_QCData).filter(PD_Protocol_QCData.id == id).first()

    def get(self, db: Session, id: Any) -> Optional[PD_Protocol_QCData]:
        """Retrieves a record based on primary key or id"""
        return db.query(PD_Protocol_QCData).filter(PD_Protocol_QCData.id == id,
                                                   PD_Protocol_QCData.isActive == True).first()

    def create(self, db: Session, *, obj_in: ProtocolQCDataCreate) -> PD_Protocol_QCData:
        db_obj = PD_Protocol_QCData(id=obj_in.id,
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
            self, db: Session, *, db_obj: PD_Protocol_QCData, obj_in: Union[ProtocolQCDataUpdate, Dict[str, Any]]
    ) -> PD_Protocol_QCData:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def insert_data(self, db: Session, data):
        db_obj = PD_Protocol_QCData(id=data['id'],
                                    userId=data['userId'],
                                    fileName=data['fileName'],
                                    documentFilePath=data['documentFilePath'],
                                    iqvdataToc=data['iqvdataToc'],
                                    iqvdataSoa=data['iqvdataSoa'],
                                    iqvdataSoaStd=str(data['iqvdataSoaStd']),
                                    iqvdataSummary=data['iqvdataSummary'],
                                    iqvdata=str(data['iqvdata']), )
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as ex:
            db.rollback()
        return db_obj

    def update_data(self, iqvdata_obj: PD_Protocol_QCData, db: Session, data):
        try:
            iqvdata_obj.id = data['id']
            iqvdata_obj.userId = data['userId']
            iqvdata_obj.fileName = data['fileName']
            iqvdata_obj.documentFilePath = data['documentFilePath']
            iqvdata_obj.iqvdataToc = data['iqvdataToc']
            iqvdata_obj.iqvdataSoa = data['iqvdataSoa']
            iqvdata_obj.iqvdataSoaStd = str(data['iqvdataSoaStd'])
            iqvdata_obj.iqvdataSummary = data['iqvdataSummary']
            iqvdata_obj.iqvdata = str(data['iqvdata'])
            db.commit()
            db.refresh(iqvdata_obj)
        except Exception as ex:
            db.rollback()
        return iqvdata_obj

    def save_qc_exceldata_to_db(self, db: Session, aidoc_id: str, iqvdata_qc_file_path: str):
        excel_data_df = pd.read_excel(iqvdata_qc_file_path, sheet_name='Sheet1')
        excel_data_df_transpose = excel_data_df.T
        keys = excel_data_df_transpose[0].tolist()
        values = excel_data_df_transpose[1].tolist()
        data = dict(zip(keys, values))
        # check any record exists with the same aidoc_id
        iqvdata_obj = self.get_by_id(db, aidoc_id)
        if iqvdata_obj is not None:
            return self.update_data(iqvdata_obj, db, data)
        else:
            return self.insert_data(db, data)

    def save_qc_jsondata_to_db(self, db: Session, aidoc_id: str, iqvdata_qc_file_path: str):
        qc_file = open(iqvdata_qc_file_path)
        data = json.load(qc_file)
        # check any record exists with the same aidoc_id
        iqvdata_obj = self.get_by_id(db, aidoc_id)
        if iqvdata_obj is not None:
            return self.update_data(iqvdata_obj, db, data)
        else:
            return self.insert_data(db, data)


pd_protocol_qcdata = CRUDProtocolQCData(PD_Protocol_QCData)
