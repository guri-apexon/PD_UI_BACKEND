from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class IqvattributeDb(SchemaBase):
   __tablename__ = "iqvattribute_db"
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
   Name = Column(TEXT)
   LocalName = Column(TEXT)
   Value = Column(TEXT)

Index('iqvattribute_db_doc_id',IqvattributeDb.doc_id)
Index('iqvattribute_db_doc_id_hierarchy',IqvattributeDb.doc_id,IqvattributeDb.hierarchy)
Index('iqvattribute_db_iqv_standard_term',IqvattributeDb.iqv_standard_term)
Index('iqvattribute_db_link_id',IqvattributeDb.link_id)
Index('iqvattribute_db_link_id_level2',IqvattributeDb.link_id_level2)
Index('iqvattribute_db_link_id_level3',IqvattributeDb.link_id_level3)
Index('iqvattribute_db_link_id_level4',IqvattributeDb.link_id_level4)
Index('iqvattribute_db_link_id_level5',IqvattributeDb.link_id_level5)
Index('iqvattribute_db_link_id_level6',IqvattributeDb.link_id_level6)
Index('iqvattribute_db_link_id_subsection1',IqvattributeDb.link_id_subsection1)
Index('iqvattribute_db_link_id_subsection2',IqvattributeDb.link_id_subsection2)
Index('iqvattribute_db_link_id_subsection3',IqvattributeDb.link_id_subsection3)
Index('iqvattribute_db_parent_id',IqvattributeDb.parent_id,IqvattributeDb.group_type)
Index('iqvattribute_db_parent_id_hierarchy',IqvattributeDb.parent_id,IqvattributeDb.hierarchy,IqvattributeDb.group_type)
