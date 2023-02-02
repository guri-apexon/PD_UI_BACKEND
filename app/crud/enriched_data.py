import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union

from app import config, crud
from app.crud.base import CRUDBase
from app.models.pd_nlp_entity import NlpentityDb
from app.schemas.pd_nlpentity import NlpEntityCreate
from app.utilities.config import settings
from app.utilities.file_utils import save_json_file
from app.utilities.pd_table_redaction import TableRedaction
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

logger = logging.getLogger(settings.LOGGER_NAME)




    def create(self, db: Session, *, obj_in: NlpEntityCreate) -> pd_nlp_entity:
        db_obj = pd_nlp_entity(id = obj_in.id,
                                    doc_id=obj_in.doc_id,
                                    link_id=obj_in.link_id,
                                    link_id_level2=obj_in.link_id_level2,
                                    link_id_level3=obj_in.link_id_level3,
                                    link_id_level4=obj_in.link_id_level4,
                                    link_id_level5=obj_in.link_id_level5,
                                    link_id_level6=obj_in.link_id_level6,
                                    link_id_subsection1=obj_in.link_id_subsection1,
                                    link_id_subsection2=obj_in.link_id_subsection2,
                                    link_id_subsection3=obj_in.link_id_subsection3,
                                    iqv_standard_term=obj_in.iqv_standard_term,
                                    parent_id=obj_in.parent_id,
                                    text=obj_in.text,
                                    user_id=obj_in.user_id,
                                    entity_class=obj_in.entity_class,
                                    entity_xref=obj_in.entity_xref,
                                    ontology=obj_in.ontology,
                                    ontology_version=obj_in.ontology_version,
                                    ontology_item_code=obj_in.ontology_item_code,
                                    standard_entity_name=obj_in.standard_entity_name, )
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
        except Exception as exc:
            logger.exception(f"Exception: str({exc})")
            db.rollback()
        return db_obj

    