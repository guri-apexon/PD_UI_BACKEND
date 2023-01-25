from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class IqvtablecolumnDb(SchemaBase):
   __tablename__ = "iqvtablecolumn_db"
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
   table_roi_id = Column(TEXT)
   minX = Column(INTEGER,nullable=False)
   maxX = Column(INTEGER,nullable=False)
   tableIndex = Column(INTEGER,nullable=False)
   tableColumnIndex = Column(INTEGER,nullable=False)
   tableColumnRef = Column(TEXT)

Index('iqvtablecolumn_db_doc_id',IqvtablecolumnDb.doc_id)
Index('iqvtablecolumn_db_doc_id_hierarchy',IqvtablecolumnDb.doc_id,IqvtablecolumnDb.hierarchy)
Index('iqvtablecolumn_db_iqv_standard_term',IqvtablecolumnDb.iqv_standard_term)
Index('iqvtablecolumn_db_link_id',IqvtablecolumnDb.link_id)
Index('iqvtablecolumn_db_link_id_level2',IqvtablecolumnDb.link_id_level2)
Index('iqvtablecolumn_db_link_id_level3',IqvtablecolumnDb.link_id_level3)
Index('iqvtablecolumn_db_link_id_level4',IqvtablecolumnDb.link_id_level4)
Index('iqvtablecolumn_db_link_id_level5',IqvtablecolumnDb.link_id_level5)
Index('iqvtablecolumn_db_link_id_level6',IqvtablecolumnDb.link_id_level6)
Index('iqvtablecolumn_db_link_id_subsection1',IqvtablecolumnDb.link_id_subsection1)
Index('iqvtablecolumn_db_link_id_subsection2',IqvtablecolumnDb.link_id_subsection2)
Index('iqvtablecolumn_db_link_id_subsection3',IqvtablecolumnDb.link_id_subsection3)
Index('iqvtablecolumn_db_parent_id',IqvtablecolumnDb.parent_id,IqvtablecolumnDb.group_type)
Index('iqvtablecolumn_db_parent_id_hierarchy',IqvtablecolumnDb.parent_id,IqvtablecolumnDb.hierarchy,IqvtablecolumnDb.group_type)
