import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union

from app import config, crud
from app.crud.base import CRUDBase
from app.models.pd_protocol_metadata import PD_Protocol_Metadata
from app.models.pd_protocol_qcdata import PD_Protocol_QCData
from app.schemas.pd_protocol_qcdata import (ProtocolQcDataCreate,
                                            ProtocolQcDataUpdate)
from app.utilities.config import settings
from app.utilities.file_utils import save_json_file
from app.utilities.pd_table_redaction import TableRedaction
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

logger = logging.getLogger(settings.LOGGER_NAME)


class CRUDProtocolQcData(CRUDBase[PD_Protocol_QCData, ProtocolQcDataCreate, ProtocolQcDataUpdate]):
    def get_by_id(self, db: Session, id: Any) -> Optional[PD_Protocol_QCData]:
        return db.query(PD_Protocol_QCData).filter(PD_Protocol_QCData.id == id).first()

    def get(self, db: Session, id: Any) -> Optional[PD_Protocol_QCData]:
        """
        Stores digitized protocol contents to file and sends the file contents
        """
        try:
            qc_resource, json_filename = self.save_db_jsondata_to_file(db = db, aidoc_id = id, file_prefix=config.QC_WIP_SRC_DB_FILE_PREFIX)
            logger.debug(f"JSON file written at: {json_filename}")
        except HTTPException as user_exception:
            raise user_exception
        except Exception as exc:
            qc_resource = None
            logger.exception(f"Exception in retrieval of data from table: {str(exc)}")

        return qc_resource

    def create(self, db: Session, *, obj_in: ProtocolQcDataCreate) -> PD_Protocol_QCData:
        db_obj = pd_protocol_qcdata(id=obj_in.id,
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
        except Exception as exc:
            logger.exception(f"Exception: str({exc})")
            db.rollback()
        return db_obj

    def update(
            self, db: Session, *, db_obj: PD_Protocol_QCData, obj_in: Union[ProtocolQcDataUpdate, Dict[str, Any]]
    ) -> PD_Protocol_QCData:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def insert_data(self, db: Session, data):
        db_obj = pd_protocol_qcdata(id=data['id'],
                                  userId=data['userId'],
                                  fileName=data['fileName'],
                                  documentFilePath=data['documentFilePath'],
                                  iqvdataToc=self.sync_toc_metadata_refresh_table_html(data['iqvdataToc'], data['iqvdataSummary']),
                                  iqvdataSoa=self.refresh_soa_table_html(data['iqvdataSoa']), #self.refresh_table_html(data['iqvdataSoa']),
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
                                detail=f"Exception in inserting JSON data into pd_protocol_qcdata {str(ex)}")
        return db_obj

    def update_data(self, iqvdata_obj: PD_Protocol_QCData, db: Session, data):
        try:
            iqvdata_obj.iqvdataToc = self.sync_toc_metadata_refresh_table_html(data['iqvdataToc'], data['iqvdataSummary'])
            iqvdata_obj.iqvdataSoa = self.refresh_soa_table_html(data['iqvdataSoa']) #self.refresh_table_html(data['iqvdataSoa'])
            iqvdata_obj.iqvdataSummary = data['iqvdataSummary']
            current_timestamp = datetime.utcnow()
            iqvdata_obj.timeUpdated = current_timestamp
            db.commit()
            db.refresh(iqvdata_obj)
        except Exception as ex:
            db.rollback()
            raise HTTPException(status_code=401,
                                detail=f"Exception in Updating Excel data into pd_protocol_qcdata {str(ex)}")
        return iqvdata_obj

    def update_iqvdata_Toc_data(self, iqvdata_obj: PD_Protocol_QCData, db: Session, data):
        try:
            iqvdata_obj.iqvdataToc = str(json.dumps(json.dumps(data)))
            db.commit()
            db.refresh(iqvdata_obj)
        except Exception as ex:
            db.rollback()
            raise HTTPException(status_code=401,
                                detail=f"Exception in Updating Excel TOC data into pd_protocol_qcdata {str(ex)}")
        return iqvdata_obj

    def refresh_toc_html_table(self, iqvdata_dict) -> dict:
        """
        Refresh HTML table
        """
        data=iqvdata_dict['data']
        field_values = iqvdata_dict['columns']
        type_idx = field_values.index('type')
        content_idx = field_values.index('content')
        len_data = len(data)
        table_counter = 0

        table_redactor = TableRedaction(redact_flag=False, hide_table_json_flag=False, return_refreshed_table_html=True)

        for idx in range(0, len_data):
            if data[idx][type_idx] == 'table' and data[idx][content_idx]:
                data[idx][content_idx] = table_redactor.redact_table(data[idx][content_idx])
                table_counter += 1
        
        logger.info(f"QC upload: Number of table HTML refreshed: {table_counter}")
        iqvdata_dict['data'] = data
        return iqvdata_dict

    def refresh_soa_table_html(self, iqvdata_soa):
        """
        Refresh table HTML
        """
        table_redactor = TableRedaction(redact_flag=False, hide_table_json_flag=False, return_refreshed_table_html=True)

        iqvdata_soa_list = json.loads(json.loads(iqvdata_soa))
        updated_iqvdata_soa_list = [table_redactor.redact_table(soa_table) for soa_table in iqvdata_soa_list]
        updated_iqvdata_soa = json.dumps(json.dumps(updated_iqvdata_soa_list))
        return updated_iqvdata_soa


    def sync_toc_metadata_refresh_table_html(self, iqvdata_toc, iqvdata_summary):
        """
        Sync up TOC metadata with User-updated-attributes
        Refresh table HTML
        """
        iqvdata_toc_dict = json.loads(json.loads(iqvdata_toc))
        logger.debug(f"iqvdataToc_dict: {iqvdata_toc_dict.keys()}")

        iqvdata_summary_dict = json.loads(json.loads(iqvdata_summary))
        logger.debug(f"iqvdataSummary_dict: {iqvdata_summary_dict.keys()}")

        # Refresh HTML table
        iqvdata_toc_dict = self.refresh_toc_html_table(iqvdata_toc_dict)

        toc_metadata_dict = iqvdata_toc_dict.get('metadata')
        for field_name, field_value, _ in iqvdata_summary_dict.get('data'):
            if field_name not in toc_metadata_dict.keys():
                logger.debug(f"\n Processing for summary attributes {field_name} ==> {field_value}")
                logger.info(f"Additional {field_name} from summary attributes added to toc_metadata")
            
            toc_metadata_dict[field_name] = field_value
        
        iqvdata_toc_dict['metadata'] = toc_metadata_dict
        updated_iqvdata_toc = json.dumps(json.dumps(iqvdata_toc_dict))
        return updated_iqvdata_toc


    def save_qc_jsondata_to_db(self, db: Session, aidoc_id: str, iqvdata_qc_file_path: str):
        """
        QC JSON details saved in DB, new QC file generated from DB and the contents sent back as response
        """
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

    def save_db_jsondata_to_file(self, db: Session, aidoc_id: str, file_prefix=config.QC_WIP_SRC_DB_FILE_PREFIX):
        """
        Extract aidoc_id contents from DB and store it in file
        Inputs: Document id
        Output 1: Returns DB contents
        Output 2: Returns stored file name

        """
        metadata_resource = crud.pd_protocol_metadata.get(db, id = aidoc_id)

        if metadata_resource is None:
            logger.warning(f"Document not active or not available [resource: {metadata_resource}]")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Document not active or not available [resource: {metadata_resource}]")

        if metadata_resource.qcStatus in ('QC1', 'QC2'):
            target_folder = Path(metadata_resource.documentFilePath).parent
            target_abs_filename = Path(target_folder, f"{file_prefix}_{aidoc_id}.json")
            qc_resource = self.get_by_id(db=db, id = aidoc_id)
            saved_file_details = save_json_file(target_folder=target_folder, target_abs_filename=target_abs_filename, data_obj = qc_resource.as_dict())
        else:
            logger.warning(f"Document not enabled to perform QC [Current qcStatus: {metadata_resource.qcStatus}]")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Document not in QC process [qcStatus: {metadata_resource.qcStatus}]")
        
        return qc_resource, saved_file_details.get('target_abs_filename')

pd_protocol_qcdata = CRUDProtocolQcData(PD_Protocol_QCData)
