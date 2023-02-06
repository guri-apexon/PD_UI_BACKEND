from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class IqvkeyvaluesetDb(SchemaBase):
   __tablename__ = "iqvkeyvalueset_db"
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
   source_system = Column(TEXT)
   key = Column(TEXT)
   value = Column(TEXT)
   confidence = Column(DOUBLE_PRECISION,nullable=False)
   rawScore = Column(DOUBLE_PRECISION,nullable=False)

Index('iqvkeyvalueset_db_doc_id',IqvkeyvaluesetDb.doc_id)
Index('iqvkeyvalueset_db_doc_id_hierarchy',IqvkeyvaluesetDb.doc_id,IqvkeyvaluesetDb.hierarchy)
Index('iqvkeyvalueset_db_iqv_standard_term',IqvkeyvaluesetDb.iqv_standard_term)
Index('iqvkeyvalueset_db_link_id',IqvkeyvaluesetDb.link_id)
Index('iqvkeyvalueset_db_link_id_level2',IqvkeyvaluesetDb.link_id_level2)
Index('iqvkeyvalueset_db_link_id_level3',IqvkeyvaluesetDb.link_id_level3)
Index('iqvkeyvalueset_db_link_id_level4',IqvkeyvaluesetDb.link_id_level4)
Index('iqvkeyvalueset_db_link_id_level5',IqvkeyvaluesetDb.link_id_level5)
Index('iqvkeyvalueset_db_link_id_level6',IqvkeyvaluesetDb.link_id_level6)
Index('iqvkeyvalueset_db_link_id_subsection1',IqvkeyvaluesetDb.link_id_subsection1)
Index('iqvkeyvalueset_db_link_id_subsection2',IqvkeyvaluesetDb.link_id_subsection2)
Index('iqvkeyvalueset_db_link_id_subsection3',IqvkeyvaluesetDb.link_id_subsection3)
Index('iqvkeyvalueset_db_parent_id',IqvkeyvaluesetDb.parent_id,IqvkeyvaluesetDb.group_type)
Index('iqvkeyvalueset_db_parent_id_hierarchy',IqvkeyvaluesetDb.parent_id,IqvkeyvaluesetDb.hierarchy,IqvkeyvaluesetDb.group_type)