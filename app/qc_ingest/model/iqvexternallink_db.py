from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class IqvexternallinkDb(SchemaBase):
   __tablename__ = "iqvexternallink_db"
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
   connection_type = Column(TEXT)
   link_text = Column(TEXT)

Index('iqvexternallink_db_doc_id',IqvexternallinkDb.doc_id)
Index('iqvexternallink_db_doc_id_hierarchy',IqvexternallinkDb.doc_id,IqvexternallinkDb.hierarchy)
Index('iqvexternallink_db_iqv_standard_term',IqvexternallinkDb.iqv_standard_term)
Index('iqvexternallink_db_link_id',IqvexternallinkDb.link_id)
Index('iqvexternallink_db_link_id_level2',IqvexternallinkDb.link_id_level2)
Index('iqvexternallink_db_link_id_level3',IqvexternallinkDb.link_id_level3)
Index('iqvexternallink_db_link_id_level4',IqvexternallinkDb.link_id_level4)
Index('iqvexternallink_db_link_id_level5',IqvexternallinkDb.link_id_level5)
Index('iqvexternallink_db_link_id_level6',IqvexternallinkDb.link_id_level6)
Index('iqvexternallink_db_link_id_subsection1',IqvexternallinkDb.link_id_subsection1)
Index('iqvexternallink_db_link_id_subsection2',IqvexternallinkDb.link_id_subsection2)
Index('iqvexternallink_db_link_id_subsection3',IqvexternallinkDb.link_id_subsection3)
Index('iqvexternallink_db_parent_id',IqvexternallinkDb.parent_id,IqvexternallinkDb.group_type)
Index('iqvexternallink_db_parent_id_hierarchy',IqvexternallinkDb.parent_id,IqvexternallinkDb.hierarchy,IqvexternallinkDb.group_type)
