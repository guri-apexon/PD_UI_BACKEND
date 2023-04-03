import logging
import uuid
from app.utilities.config import settings
from app.models.pd_labsparameter_db import IqvlabparameterrecordDb
from app.schemas.pd_labdata import LabDataCreate, LabDataUpdate
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from fastapi import HTTPException
from etmfa_core.aidoc.io import set_labparameterrecord_with_id
from datetime import datetime
from app.db.session import psqlengine


logger = logging.getLogger(settings.LOGGER_NAME)


class LabDataCrud(CRUDBase[IqvlabparameterrecordDb, LabDataCreate, LabDataUpdate]):
    """
    Lab data crud operation
    """

    @staticmethod
    def get_records(db: Session, doc_id: str):
        """ fetch record with lab data"""
        lab_data_rec = []
        try:
            lab_data_rec = db.query(IqvlabparameterrecordDb).filter(
                IqvlabparameterrecordDb.doc_id == doc_id
            ).all()
        except Exception as ex:
            logger.exception("Exception in retrieval of data from table", ex)
            raise HTTPException(status_code=400,
                                detail=f"Exception to get lab data {str(ex)}")
        return lab_data_rec

    def save_data_to_db(self, db: Session, data):
        """ To create new record with lab data """
        try:
            new_entity = IqvlabparameterrecordDb(id=str(uuid.uuid1()),
                                                 doc_id=data.doc_id,
                                                 run_id=data.run_id,
                                                 parameter=data.parameter,
                                                 parameter_text=data.parameter_text,
                                                 procedure_panel=data.procedure_panel,
                                                 procedure_panel_text=data.procedure_panel_text,
                                                 assessment=data.assessment,
                                                 dts=data.dts,
                                                 pname=data.pname,
                                                 ProcessMachineName=data.ProcessMachineName,
                                                 ProcessVersion=data.ProcessVersion,
                                                 roi_id=str(uuid.uuid1()),
                                                 section=data.section,
                                                 table_link_text=data.table_link_text,
                                                 table_roi_id=data.table_roi_id,
                                                 table_sequence_index=data.table_sequence_index
                                                 )
            db.add(new_entity)
            db.commit()
            db.refresh(new_entity)

            results = {'doc_id': new_entity.doc_id,
                       'run_id': new_entity.run_id,
                       "procedure_panel_text": new_entity.procedure_panel_text,
                       "assessment": new_entity.assessment,
                       "table_roi_id": new_entity.table_roi_id,
                       "table_sequence_index": new_entity.table_sequence_index,
                       "table_link_text": new_entity.table_link_text,
                       "parameter_text": new_entity.parameter_text,
                       "pname": new_entity.pname,
                       "roi_id": new_entity.roi_id,
                       'id': [new_entity.id]}
            return results
        except Exception as ex:
            db.rollback()
            raise HTTPException(status_code=406, detail=f"Exception in Saving JSON data to DB {str(ex)}")

    @staticmethod
    def update_data_db(data):
        try:
            for dt in data:
                connection = psqlengine.raw_connection()
                doc_id = dt.doc_id
                source_roi_id = dt.roi_id
                table_link_text = dt.table_link_text
                table_roi_id = dt.table_roi_id
                assessment = dt.assessment
                procedure_panel = dt.procedure_panel
                procedure_panel_text = dt.procedure_panel_text
                parameter = dt.parameter
                parameter_text = dt.parameter_text
                code_version = ''
                date = datetime.utcnow()
                dts = '{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(
                    date.year, date.month, date.day, date.hour, date.minute, date.second)
                [b_updated, num_rows_updated] = set_labparameterrecord_with_id(
                    connection,
                    doc_id,
                    source_roi_id=source_roi_id,
                    table_link_text=table_link_text,
                    table_roi_id=table_roi_id,
                    assessment=assessment,
                    procedure_panel=procedure_panel,
                    procedure_panel_text=procedure_panel_text,
                    parameter=parameter,
                    parameter_text=parameter_text,
                    code_version=code_version,
                    dts=dts
                )
                if not b_updated:
                    raise HTTPException(status_code=304, detail=f"Exception in Updating JSON data to ")

            return True
        except Exception as ex:
            logger.exception("Exception in updating data from table", ex)
            raise HTTPException(status_code=406, detail=f"Exception in Updating JSON data to DB {str(ex)}")

    @staticmethod
    def delete_data_db(db: Session, data):
        doc_id = data.doc_id
        table_roi_id = data.table_roi_id
        roi_id = data.roi_id

        try:
            entity_rec = db.query(IqvlabparameterrecordDb).filter(
                IqvlabparameterrecordDb.doc_id == doc_id,
                IqvlabparameterrecordDb.table_roi_id == table_roi_id,
                IqvlabparameterrecordDb.roi_id == roi_id
            ).update({
                'soft_delete': 1
            })
            db.commit()
            if entity_rec > 0:
                return entity_rec
            else:
                raise HTTPException(status_code=304, detail=f"No Record Updated")

        except Exception as ex:
            db.rollback()
            raise HTTPException(status_code=406, detail=f"Exception in deleting JSON data to DB {str(ex)}")


labdata_content = LabDataCrud(IqvlabparameterrecordDb)
