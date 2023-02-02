from typing import Optional

from pydantic import BaseModel


# Shared properties
class NlpEntityBase(BaseModel):
    id: Optional[str] = None
    doc_id: Optional[str] = None
    link_id: Optional[str] = None
    link_id_level2: Optional[str] = None
    link_id_level3: Optional[str] = None
    link_id_level4: Optional[str] = None
    link_id_level5: Optional[str] = None
    link_id_level6: Optional[str] = None
    link_id_subsection1: Optional[str] = None
    link_id_subsection2: Optional[str] = None
    link_id_subsection3: Optional[str] = None
    iqv_standard_term: Optional[str] = None
    parent_id: Optional[str] = None
    text: Optional[str] = None
    user_id: Optional[str] = None
    entity_class: Optional[str] = None
    entity_xref: Optional[str] = None
    ontology: Optional[str] = None
    ontology_version: Optional[str] = None
    ontology_item_code: Optional[str] = None
    standard_entity_name: Optional[str] = None
    


# Properties to receive via API on creation
class NlpEntityCreate(NlpEntityBase):
    id: str 
    doc_id: str
    link_id: str
    link_id_level2: str
    link_id_level3: str
    link_id_level4: str
    link_id_level5: str
    link_id_level6: str
    link_id_subsection1: str
    link_id_subsection2: str
    link_id_subsection3: str
    iqv_standard_term: str
    parent_id: str
    text: str
    user_id: str
    entity_class: str
    entity_xref: str
    ontology: str
    ontology_version: str
    ontology_item_code: str
    standard_entity_name: str
    



