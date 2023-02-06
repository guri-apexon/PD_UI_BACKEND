from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class IqvqcupdatetrackingDb(SchemaBase):
   __tablename__ = "iqvqcupdatetracking_db"
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
   QC_id = Column(TEXT)
   QCType = Column(TEXT)
   seq_num = Column(INTEGER,nullable=False)
   user_id = Column(TEXT)
   source_system = Column(TEXT)
   dts = Column(TEXT)
   OriginalText = Column(TEXT)
   UpdatedText = Column(TEXT)
   roi_id = Column(TEXT)
   ItemDataType = Column(TEXT)

Index('iqvqcupdatetracking_db_doc_id',IqvqcupdatetrackingDb.doc_id)
Index('iqvqcupdatetracking_db_doc_id_hierarchy',IqvqcupdatetrackingDb.doc_id,IqvqcupdatetrackingDb.hierarchy)
Index('iqvqcupdatetracking_db_iqv_standard_term',IqvqcupdatetrackingDb.iqv_standard_term)
Index('iqvqcupdatetracking_db_link_id',IqvqcupdatetrackingDb.link_id)
Index('iqvqcupdatetracking_db_link_id_level2',IqvqcupdatetrackingDb.link_id_level2)
Index('iqvqcupdatetracking_db_link_id_level3',IqvqcupdatetrackingDb.link_id_level3)
Index('iqvqcupdatetracking_db_link_id_level4',IqvqcupdatetrackingDb.link_id_level4)
Index('iqvqcupdatetracking_db_link_id_level5',IqvqcupdatetrackingDb.link_id_level5)
Index('iqvqcupdatetracking_db_link_id_level6',IqvqcupdatetrackingDb.link_id_level6)
Index('iqvqcupdatetracking_db_link_id_subsection1',IqvqcupdatetrackingDb.link_id_subsection1)
Index('iqvqcupdatetracking_db_link_id_subsection2',IqvqcupdatetrackingDb.link_id_subsection2)
Index('iqvqcupdatetracking_db_link_id_subsection3',IqvqcupdatetrackingDb.link_id_subsection3)
Index('iqvqcupdatetracking_db_parent_id',IqvqcupdatetrackingDb.parent_id,IqvqcupdatetrackingDb.group_type)
Index('iqvqcupdatetracking_db_parent_id_hierarchy',IqvqcupdatetrackingDb.parent_id,IqvqcupdatetrackingDb.hierarchy,IqvqcupdatetrackingDb.group_type)