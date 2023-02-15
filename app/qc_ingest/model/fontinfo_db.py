from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class FontinfoDb(SchemaBase):
   __tablename__ = "fontinfo_db"
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
   Bold = Column(BOOLEAN,nullable=False)
   Italics = Column(BOOLEAN,nullable=False)
   Caps = Column(BOOLEAN,nullable=False)
   ColorRGB = Column(INTEGER,nullable=False)
   DStrike = Column(BOOLEAN,nullable=False)
   Emboss = Column(BOOLEAN,nullable=False)
   Imprint = Column(BOOLEAN,nullable=False)
   Outline = Column(BOOLEAN,nullable=False)
   rStyle = Column(TEXT)
   Shadow = Column(BOOLEAN,nullable=False)
   SmallCaps = Column(BOOLEAN,nullable=False)
   Strike = Column(BOOLEAN,nullable=False)
   Highlight = Column(TEXT)
   Size = Column(INTEGER,nullable=False)
   Underline = Column(TEXT)
   Vanish = Column(BOOLEAN,nullable=False)
   rFonts = Column(TEXT)
   VertAlign = Column(TEXT)

   def as_dict(self):
      obj = {c.name: getattr(self, c.name) for c in self.__table__.columns}
      return obj

Index('fontinfo_db_doc_id',FontinfoDb.doc_id)
Index('fontinfo_db_doc_id_hierarchy',FontinfoDb.doc_id,FontinfoDb.hierarchy)
Index('fontinfo_db_iqv_standard_term',FontinfoDb.iqv_standard_term)
Index('fontinfo_db_link_id',FontinfoDb.link_id)
Index('fontinfo_db_link_id_level2',FontinfoDb.link_id_level2)
Index('fontinfo_db_link_id_level3',FontinfoDb.link_id_level3)
Index('fontinfo_db_link_id_level4',FontinfoDb.link_id_level4)
Index('fontinfo_db_link_id_level5',FontinfoDb.link_id_level5)
Index('fontinfo_db_link_id_level6',FontinfoDb.link_id_level6)
Index('fontinfo_db_link_id_subsection1',FontinfoDb.link_id_subsection1)
Index('fontinfo_db_link_id_subsection2',FontinfoDb.link_id_subsection2)
Index('fontinfo_db_link_id_subsection3',FontinfoDb.link_id_subsection3)
Index('fontinfo_db_parent_id',FontinfoDb.parent_id,FontinfoDb.group_type)
Index('fontinfo_db_parent_id_hierarchy',FontinfoDb.parent_id,FontinfoDb.hierarchy,FontinfoDb.group_type)
