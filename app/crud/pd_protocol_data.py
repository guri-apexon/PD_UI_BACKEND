import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union

import pandas as pd
import requests
from app import config, crud
from app.crud.base import CRUDBase
from app.models.pd_protocol_data import PD_Protocol_Data
from app.models.pd_protocol_metadata import PD_Protocol_Metadata
from app.models.pd_protocol_qcdata import PD_Protocol_QCData
from app.schemas.pd_protocol_data import ProtocolDataCreate, ProtocolDataUpdate
from app.utilities.config import settings
from app.utilities.file_utils import (save_json_file, write_data_to_json,
                                      write_data_to_xlsx)
from fastapi import HTTPException
from sqlalchemy.orm import Session

logger = logging.getLogger(settings.LOGGER_NAME)


class CRUDProtocolData(CRUDBase[PD_Protocol_Data, ProtocolDataCreate, ProtocolDataUpdate]):
    def get_by_id(self, db: Session, id: Any) -> Optional[PD_Protocol_Data]:
        return db.query(PD_Protocol_Data).filter(PD_Protocol_Data.id == id).first()

    def get(self, db: Session, id: Any, user: Any) -> Optional[PD_Protocol_Data]:
        """Retrieves a record based on primary key or id"""
        try:
            resource = db.query(PD_Protocol_Metadata).filter(PD_Protocol_Metadata.id == id, PD_Protocol_Metadata.isActive == True).first()
            if resource is None:
                return resource
            if user == 'normal':
                resource = db.query(PD_Protocol_Data).filter(PD_Protocol_Data.id == id).first()
            else:
                logger.error(f"No such user type exists in DB: {user}")
                raise Exception
        except Exception as ex:
            resource = None
            logger.exception("Exception in retrieval of data from table", ex)
        return resource

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

    def insert_data(self, db: Session, data):
        db_obj = PD_Protocol_Data(id=data['id'],
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
            raise HTTPException(status_code=401,
                                detail=f"Exception in inserting JSON data into PD_Protocol_Data {str(ex)}")
        return db_obj

    def update_data(self, iqvdata_obj: PD_Protocol_Data, db: Session, data):
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
            current_timestamp = datetime.utcnow()
            iqvdata_obj.timeUpdated = current_timestamp
            db.commit()
            db.refresh(iqvdata_obj)
        except Exception as ex:
            db.rollback()
            raise HTTPException(status_code=401,
                                detail=f"Exception in Updating Excel data into PD_Protocol_Data {str(ex)}")
        return iqvdata_obj

    def update_iqvdata_Toc_data(self, iqvdata_obj: PD_Protocol_Data, db: Session, data):
        try:
            iqvdata_obj.iqvdataToc = str(json.dumps(json.dumps(data)))
            db.commit()
            db.refresh(iqvdata_obj)
        except Exception as ex:
            db.rollback()
            raise HTTPException(status_code=401,
                                detail=f"Exception in Updating Excel TOC data into PD_Protocol_Data {str(ex)}")
        return iqvdata_obj

    def save_qc_exceldata_to_db(self, db: Session, aidoc_id: str, iqvdata_qc_file_path: str):
        try:
            excel_data_toc_df = pd.read_excel(iqvdata_qc_file_path, sheet_name='TOC')
            excel_data_toc_df.fillna(value='', inplace=True)
            # Build dict
            updated_file_dict = excel_data_toc_df.to_dict(orient="split")
            iqvdata_obj = self.get_by_id(db, aidoc_id)
            if iqvdata_obj is not None:
                self.update_iqvdata_Toc_data(iqvdata_obj, db, updated_file_dict)
            else:
                raise HTTPException(status_code=402,
                                    detail=f"Exception in saving excel TOC data to DB - iqvdata_obj is None")
        except Exception as ex:
            raise HTTPException(status_code=401, detail=f"Exception in uploaded Excel File {str(ex)}")

        return True

    def save_qc_jsondata_to_db(self, db: Session, aidoc_id: str, iqvdata_qc_file_path: str):
        try:
            qc_file = open(iqvdata_qc_file_path)
            data = json.load(qc_file)
            iqvdata_obj = self.get_by_id(db, aidoc_id)
            if iqvdata_obj is not None:
                return self.update_data(iqvdata_obj, db, data)
            else:
                return self.insert_data(db, data)
        except Exception as ex:
            raise HTTPException(status_code=401, detail=f"Exception in Saving JSON data to DB {str(ex)}")

    def generate_iqvdata_json_file(self, aidoc_id: str):
        try:
            PARAMS = {'id': aidoc_id}
            r = requests.get(url=settings.PROTOCOL_DATA_API_URL, params=PARAMS)
            data = r.json()
            if data is not None:
                json_path = write_data_to_json(aidoc_id, data)
                return json_path
            else:
                raise HTTPException(status_code=401, detail=f"Error in Generating json file, No data found.")
        except Exception as ex:
            raise HTTPException(status_code=402, detail=f"Exception occured in generating iqvdata-json-file {str(ex)}")

    def generate_iqvdata_xlsx_file(self, aidoc_id: str):
        try:
            PARAMS = {'id': aidoc_id}
            r = requests.get(url=settings.PROTOCOL_DATA_API_URL, params=PARAMS)
            data = r.json()
            if data is not None:
                xlsx_path = write_data_to_xlsx(aidoc_id, data)
                return xlsx_path
            else:
                raise HTTPException(status_code=401, detail=f"Error in Generating xlsx file, No data found.")
        except Exception as ex:
            raise HTTPException(status_code=402, detail=f"Exception occured in generating iqvdata-excel-file {str(ex)}")

    def save_db_jsondata_to_dig_file(self, db: Session, aidoc_id: str, target_folder: str, file_prefix=config.DIG_FILE_PREFIX):
        """
        Extract aidoc_id contents from DB and store it in file
        Inputs: Document id and optional file prefix
        Output: Returns stored file name

        """
        target_abs_filename = Path(target_folder, f"{file_prefix}_{aidoc_id}.json")
        data_resource = self.get_by_id(db=db, id = aidoc_id)
        saved_file_details = save_json_file(target_folder=target_folder, target_abs_filename=target_abs_filename, data_obj = data_resource.as_dict())
        
        return saved_file_details.get('target_abs_filename')
  
pd_protocol_data = CRUDProtocolData(PD_Protocol_Data)
