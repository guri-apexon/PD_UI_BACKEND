from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class IqvexternallinkelementDb(SchemaBase):
   __tablename__ = "iqvexternallinkelement_db"
   id = Column(VARCHAR(128),primary_key=True,nullable=False)
   doc_id = Column(TEXT)
   link_id = Column(TEXT)
   link_id_level2 = Column(TEXT)
   link_id_level3 = Column(TEXT)
   link_id_level4 = Column(TEXT)
   link_id_level5 = Column(TEXT)
   link_id_level6 = Column(TEXT)
   link_id_subsection1 = Column(TEXT)
   link_id_subsection2 = Column(TEXT)
   link_id_subsection3 = Column(TEXT)
   hierarchy = Column(VARCHAR(128),primary_key=True,nullable=False)
   iqv_standard_term = Column(TEXT)
   parent_id = Column(TEXT)
   group_type = Column(TEXT)
   text = Column(TEXT)
   startIndex = Column(INTEGER,nullable=False)
   length = Column(INTEGER,nullable=False)

Index('iqvexternallinkelement_db_doc_id',IqvexternallinkelementDb.doc_id)
Index('iqvexternallinkelement_db_doc_id_hierarchy',IqvexternallinkelementDb.doc_id,IqvexternallinkelementDb.hierarchy)
Index('iqvexternallinkelement_db_iqv_standard_term',IqvexternallinkelementDb.iqv_standard_term)
Index('iqvexternallinkelement_db_link_id',IqvexternallinkelementDb.link_id)
Index('iqvexternallinkelement_db_link_id_level2',IqvexternallinkelementDb.link_id_level2)
Index('iqvexternallinkelement_db_link_id_level3',IqvexternallinkelementDb.link_id_level3)
Index('iqvexternallinkelement_db_link_id_level4',IqvexternallinkelementDb.link_id_level4)
Index('iqvexternallinkelement_db_link_id_level5',IqvexternallinkelementDb.link_id_level5)
Index('iqvexternallinkelement_db_link_id_level6',IqvexternallinkelementDb.link_id_level6)
Index('iqvexternallinkelement_db_link_id_subsection1',IqvexternallinkelementDb.link_id_subsection1)
Index('iqvexternallinkelement_db_link_id_subsection2',IqvexternallinkelementDb.link_id_subsection2)
Index('iqvexternallinkelement_db_link_id_subsection3',IqvexternallinkelementDb.link_id_subsection3)
Index('iqvexternallinkelement_db_parent_id',IqvexternallinkelementDb.parent_id,IqvexternallinkelementDb.group_type)
Index('iqvexternallinkelement_db_parent_id_hierarchy',IqvexternallinkelementDb.parent_id,IqvexternallinkelementDb.hierarchy,IqvexternallinkelementDb.group_type)
