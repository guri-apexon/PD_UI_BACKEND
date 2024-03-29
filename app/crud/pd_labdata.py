import logging
import uuid
from app.utilities.config import settings
from app.models.pd_labsparameter_db import IqvlabparameterrecordDb
from app.schemas.pd_labdata import LabDataCreate, LabDataUpdate
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from fastapi import HTTPException
from etmfa_core.aidoc.io import set_labparameterrecord_with_id
from datetime import datetime, timezone
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
                IqvlabparameterrecordDb.doc_id == doc_id,
                IqvlabparameterrecordDb.soft_delete == None
            ).all()
        except Exception as ex:
            logger.exception("Exception in retrieval of data from table", ex)
            raise HTTPException(status_code=400,
                                detail=f"Exception to get lab data {str(ex)}")
        return lab_data_rec

    @staticmethod
    def save_data_to_db(db: Session, arr_data):
        """ To create new record with lab data """
        try:
            objects = []
            for data in arr_data:
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
                objects.append(new_entity)

            db.bulk_save_objects(objects)
            db.commit()

            return True
        except Exception as ex:
            db.rollback()
            raise HTTPException(status_code=406, detail=f"Exception in Saving JSON data to DB {str(ex)}")

    @staticmethod
    def update_data_db(db, arr_data):
        try:
            for dt in arr_data:
                column_id = dt.id
                table_link_text = dt.table_link_text
                assessment = dt.assessment
                procedure_panel = dt.procedure_panel
                procedure_panel_text = dt.procedure_panel_text
                parameter = dt.parameter
                parameter_text = dt.parameter_text
                pname = dt.pname
                date = datetime.utcnow()
                dts = '{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}'.format(
                    date.year, date.month, date.day, date.hour, date.minute, date.second)
                entity_rec = db.query(IqvlabparameterrecordDb).filter(
                    IqvlabparameterrecordDb.id == column_id
                ).update({
                    'table_link_text': table_link_text,
                    'assessment': assessment,
                    'procedure_panel': procedure_panel,
                    'procedure_panel_text': procedure_panel_text,
                    'parameter': parameter,
                    'parameter_text': parameter_text,
                    'dts': dts,
                    'pname': pname
                })
                db.flush()

            db.commit()
            return True

        except Exception as ex:
            logger.exception("Exception in updating data from table {}".format(ex))
            raise HTTPException(status_code=406, detail=f"Exception in Updating JSON data to DB {str(ex)}")

    @staticmethod
    def delete_data_db(db: Session, arr_data):
        try:
            for data in arr_data:
                doc_id = data.doc_id
                table_roi_id = data.table_roi_id
                roi_id = data.roi_id

                entity_rec = db.query(IqvlabparameterrecordDb).filter(
                    IqvlabparameterrecordDb.doc_id == doc_id,
                    IqvlabparameterrecordDb.table_roi_id == table_roi_id,
                    IqvlabparameterrecordDb.roi_id == roi_id
                ).update({
                    'soft_delete': 1
                })
                db.flush()

            db.commit()
            return True
        except Exception as ex:
            db.rollback()
            raise HTTPException(status_code=406, detail=f"Exception in deleting JSON data to DB {str(ex)}")

    def create_lab_data_table(self, db: Session, dt):

        records = self.get_records(db, dt.doc_id)
        if not records:

            table_roi_id = str(uuid.uuid1())
            roi_id = str(uuid.uuid1())
            try:
                connection = psqlengine.raw_connection()
                doc_id = dt.doc_id
                source_roi_id = roi_id
                table_link_text = "" if not dt.table_link_text else dt.table_link_text
                table_roi_id = table_roi_id
                assessment = "" if not dt.assessment else dt.assessment
                procedure_panel = "" if not dt.procedure_panel else dt.procedure_panel
                procedure_panel_text = "" if not dt.procedure_panel_text else dt.procedure_panel_text
                parameter = "" if not dt.parameter else dt.parameter
                parameter_text = "" if not dt.parameter_text else dt.parameter_text
                code_version = 'UI.labs.1.1'
                date = datetime.now(timezone.utc)
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

                lab_data_rec = db.query(IqvlabparameterrecordDb).filter(
                    IqvlabparameterrecordDb.doc_id == doc_id,
                    IqvlabparameterrecordDb.table_roi_id == table_roi_id
                ).first()
                return [{
                    "parameter": "",
                    "doc_id": doc_id,
                    "parameter_text": "",
                    "procedure_panel_text": "",
                    "dts": "",
                    "ProcessMachineName": "",
                    "roi_id": roi_id,
                    "table_link_text": "",
                    "table_sequence_index": -1,
                    "id": lab_data_rec.id,
                    "run_id": "",
                    "procedure_panel": "",
                    "assessment": "",
                    "pname": "",
                    "ProcessVersion": "",
                    "section": "",
                    "table_roi_id": table_roi_id,
                    "soft_delete": None
                }]
            except Exception as ex:
                logger.exception("Exception in updating data from table", ex)
                raise HTTPException(status_code=406, detail=f"Exception in Updating JSON data to DB {str(ex)}")

        return records


labdata_content = LabDataCrud(IqvlabparameterrecordDb)

