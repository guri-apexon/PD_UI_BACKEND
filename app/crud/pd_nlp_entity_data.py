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
                NlpEntityDb.link_id == link_id).all()
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
            ).all()
        except Exception as ex:
            logger.exception("Exception in retrieval of data from table", ex)
        return entity_rec

    @staticmethod
    def insert_data(entity_obj: NlpEntityDb, db: Session, data):
        """ To create new records with updated clinical terms"""
        synonyms = data.entity_xref or entity_obj.entity_xref
        preferred_term = data.iqv_standard_term or entity_obj.iqv_standard_term
        classification = data.entity_class or entity_obj.entity_class
        ontology = data.ontology or entity_obj.ontology

        new_entity = NlpEntityDb(id=str(uuid.uuid1()),
                                 doc_id=entity_obj.doc_id,
                                 link_id=entity_obj.link_id,
                                 link_id_level2=entity_obj.link_id_level2,
                                 link_id_level3=entity_obj.link_id_level3,
                                 link_id_level4=entity_obj.link_id_level4,
                                 link_id_level5=entity_obj.link_id_level5,
                                 link_id_level6=entity_obj.link_id_level6,
                                 link_id_subsection1=entity_obj.link_id_subsection1,
                                 link_id_subsection2=entity_obj.link_id_subsection2,
                                 link_id_subsection3=entity_obj.link_id_subsection3,
                                 hierarchy=entity_obj.hierarchy,
                                 iqv_standard_term=preferred_term,
                                 parent_id=entity_obj.parent_id,
                                 group_type=entity_obj.group_type,
                                 process_source=entity_obj.process_source,
                                 text=entity_obj.text,
                                 user_id=entity_obj.user_id,
                                 entity_class=classification,
                                 entity_xref=synonyms,
                                 ontology=ontology,
                                 ontology_version=entity_obj.ontology_version,
                                 ontology_item_code=entity_obj.ontology_item_code,
                                 standard_entity_name=entity_obj.standard_entity_name,
                                 confidence=entity_obj.confidence,
                                 start=entity_obj.start,
                                 text_len=entity_obj.text_len)
        try:
            db.add(new_entity)
            db.commit()
            db.refresh(new_entity)
        except Exception as ex:
            db.rollback()
            raise HTTPException(status_code=401,
                                detail=f"Exception to create entity data {str(ex)}")
        return new_entity

    def save_data_to_db(self, db: Session, aidoc_id: str, link_id: str, data):
        """ To create new record with updated clinical terms based on enriched
        text, apart from keep existing record data """
        try:
            entity_text = data.standard_entity_name
            entity_objs = self.get_records(db, aidoc_id, link_id, entity_text)
            results = {}
            for entity_obj in entity_objs:
                db_record = self.insert_data(entity_obj, db, data)
                if 'id' in results:
                    results.get('id').append(db_record.id)
                else:
                    results = {'doc_id': db_record.doc_id,
                               'link_id': db_record.link_id,
                               "standard_entity_name": db_record.standard_entity_name,
                               "iqv_standard_term": db_record.iqv_standard_term,
                               "entity_class": db_record.entity_class,
                               "entity_xref": db_record.entity_xref,
                               "ontology": db_record.ontology,
                               'id': [db_record.id]}
            return results
        except Exception as ex:
            raise HTTPException(status_code=401, detail=f"Exception in Saving JSON data to DB {str(ex)}")


nlp_entity_content = NlpEntityCrud(NlpEntityDb)
