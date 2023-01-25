from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class DocumentpartslistDb(SchemaBase):
   __tablename__ = "documentpartslist_db"
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
   hierarchy = Column(VARCHAR(128),nullable=False)
   iqv_standard_term = Column(TEXT)
   parent_id = Column(TEXT)
   group_type = Column(TEXT)
   sequence_id = Column(INTEGER,nullable=False)

Index('documentpartslist_db_doc_id',DocumentpartslistDb.doc_id)
Index('documentpartslist_db_doc_id_hierarchy',DocumentpartslistDb.doc_id,DocumentpartslistDb.hierarchy)
Index('documentpartslist_db_iqv_standard_term',DocumentpartslistDb.iqv_standard_term)
Index('documentpartslist_db_link_id',DocumentpartslistDb.link_id)
Index('documentpartslist_db_link_id_level2',DocumentpartslistDb.link_id_level2)
Index('documentpartslist_db_link_id_level3',DocumentpartslistDb.link_id_level3)
Index('documentpartslist_db_link_id_level4',DocumentpartslistDb.link_id_level4)
Index('documentpartslist_db_link_id_level5',DocumentpartslistDb.link_id_level5)
Index('documentpartslist_db_link_id_level6',DocumentpartslistDb.link_id_level6)
Index('documentpartslist_db_link_id_subsection1',DocumentpartslistDb.link_id_subsection1)
Index('documentpartslist_db_link_id_subsection2',DocumentpartslistDb.link_id_subsection2)
Index('documentpartslist_db_link_id_subsection3',DocumentpartslistDb.link_id_subsection3)
Index('documentpartslist_db_parent_id',DocumentpartslistDb.parent_id,DocumentpartslistDb.group_type)
Index('documentpartslist_db_parent_id_hierarchy',DocumentpartslistDb.parent_id,DocumentpartslistDb.hierarchy,DocumentpartslistDb.group_type)
