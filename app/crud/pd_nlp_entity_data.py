from datetime import datetime, timezone
import logging
import uuid
from app.utilities.config import settings
from app.models.pd_nlp_entity_db import NlpEntityDb
from app.schemas.pd_nlp_entity_db import NlpEntityCreate, NlpEntityUpdate
from app.crud.base import CRUDBase
from sqlalchemy.orm import Session
from fastapi import HTTPException

logger = logging.getLogger(settings.LOGGER_NAME)


class NlpEntityCrud(CRUDBase[NlpEntityDb, NlpEntityCreate, NlpEntityUpdate]):
    """
    NLP Entity crud operation to get entity object with clinical terms.
    """
    def get(self, db: Session, doc_id: str, link_id: str):
        try:
            all_term_data = db.query(NlpEntityDb).filter(
                NlpEntityDb.doc_id == doc_id).filter(
                NlpEntityDb.link_id == link_id).distinct(NlpEntityDb.parent_id).all()
        except Exception as ex:
            all_term_data = []
            logger.exception("Exception in retrieval of data from table", ex)
        return all_term_data

    @staticmethod
    def get_records(db: Session, doc_id: str, link_id: str, entity_text: str):
        """ To fetch records based on doc, link and entity text """
        entity_rec = []
        try:
            entity_rec = db.query(NlpEntityDb).filter(
                NlpEntityDb.doc_id == doc_id).filter(
                NlpEntityDb.link_id == link_id).filter(
                NlpEntityDb.standard_entity_name == entity_text
            ).distinct(NlpEntityDb.parent_id).all()
        except Exception as ex:
            logger.exception("Exception in retrieval of data from table", ex)
        return entity_rec

    @staticmethod
    def insert_nlp_data(db: Session, doc_id, link_id, data, entity_obj=None):
        """ To create new records with updated terms"""
        synonyms = data.entity_xref or ""
        preferred_term = data.iqv_standard_term or ""
        classification = data.entity_class or ""
        ontology = data.ontology or ""
        clinical_terms = data.clinical_terms or ""

        data = entity_obj if entity_obj else data
        new_entity = NlpEntityDb(id=str(uuid.uuid1()),
                                 doc_id=doc_id,
                                 link_id=link_id,
                                 link_id_level2=data.link_id_level2,
                                 link_id_level3=data.link_id_level3,
                                 link_id_level4=data.link_id_level4,
                                 link_id_level5=data.link_id_level5,
                                 link_id_level6=data.link_id_level6,
                                 link_id_subsection1=data.link_id_subsection1,
                                 link_id_subsection2=data.link_id_subsection2,
                                 link_id_subsection3=data.link_id_subsection3,
                                 hierarchy=data.hierarchy,
                                 iqv_standard_term=preferred_term,
                                 parent_id=data.parent_id,
                                 group_type=data.group_type,
                                 process_source=data.process_source,
                                 text=clinical_terms,
                                 user_id=data.user_id,
                                 entity_class=classification,
                                 entity_xref=synonyms,
                                 ontology=ontology,
                                 ontology_version=data.ontology_version,
                                 ontology_item_code=data.ontology_item_code,
                                 standard_entity_name=data.standard_entity_name,
                                 confidence=data.confidence,
                                 start=data.start,
                                 text_len=len(data.standard_entity_name),
                                 dts=datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S"))
        try:
            db.add(new_entity)
            db.commit()
            db.refresh(new_entity)
        except Exception as ex:
            db.rollback()
            raise HTTPException(status_code=401,
                                detail=f"Exception to create entity data {str(ex)}")
        return new_entity

    def save_data_to_db(self, db: Session, aidoc_id: str, link_id: str, operation_type: str, data):
        """ To create new record with updated clinical terms based on enriched
        text, apart from keep existing record data """
        try:
            entity_text = data.standard_entity_name
            entity_objs = self.get_records(db, aidoc_id, link_id, entity_text)
            results = {}
            if not entity_objs:
                db_record = self.insert_nlp_data(db, aidoc_id, link_id, data)
                results = {'doc_id': db_record.doc_id,
                           'link_id': db_record.link_id,
                           "standard_entity_name": db_record.standard_entity_name,
                           "iqv_standard_term": db_record.iqv_standard_term,
                           "entity_class": db_record.entity_class,
                           "entity_xref": db_record.entity_xref,
                           "ontology": db_record.ontology,
                           'id': [db_record.id]}
            else:
                db_record = None
                for entity_obj in entity_objs:
                    if operation_type == "delete":
                        db_record = self.insert_nlp_data(db, aidoc_id, link_id, data)
                    else:
                        db_record = self.insert_nlp_data(db, aidoc_id, link_id, data)

                    db_obj = db_record if db_record else entity_obj
                    if 'id' in results:
                        results.get('id').append(db_obj.id)
                    else:
                        results = {'doc_id': db_obj.doc_id,
                                   'link_id': db_obj.link_id,
                                   "standard_entity_name": db_obj.standard_entity_name,
                                   "iqv_standard_term": db_obj.iqv_standard_term,
                                   "entity_class": db_obj.entity_class,
                                   "entity_xref": db_obj.entity_xref,
                                   "ontology": db_obj.ontology,
                                   'id': [db_obj.id]}
                db.commit()
            return results
        except Exception as ex:
            raise HTTPException(status_code=401, detail=f"Exception in Saving JSON data to DB {str(ex)}")


nlp_entity_content = NlpEntityCrud(NlpEntityDb)
