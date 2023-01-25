from sqlalchemy import Column,Index
from .__base__ import SchemaBase
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION,TEXT,VARCHAR,INTEGER,BOOLEAN,BIGINT,JSONB,BYTEA

class NlpSegmentDb(SchemaBase):
   __tablename__ = "nlp_segment_db"
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
   segment_type = Column(TEXT)
   text = Column(TEXT)
   text_footnotes_list = Column(TEXT)
   primary_section = Column(TEXT)
   secondary_section = Column(TEXT)

Index('nlp_segment_db_doc_id',NlpSegmentDb.doc_id)
Index('nlp_segment_db_doc_id_hierarchy',NlpSegmentDb.doc_id,NlpSegmentDb.hierarchy)
Index('nlp_segment_db_iqv_standard_term',NlpSegmentDb.iqv_standard_term)
Index('nlp_segment_db_link_id',NlpSegmentDb.link_id)
Index('nlp_segment_db_link_id_level2',NlpSegmentDb.link_id_level2)
Index('nlp_segment_db_link_id_level3',NlpSegmentDb.link_id_level3)
Index('nlp_segment_db_link_id_level4',NlpSegmentDb.link_id_level4)
Index('nlp_segment_db_link_id_level5',NlpSegmentDb.link_id_level5)
Index('nlp_segment_db_link_id_level6',NlpSegmentDb.link_id_level6)
Index('nlp_segment_db_link_id_subsection1',NlpSegmentDb.link_id_subsection1)
Index('nlp_segment_db_link_id_subsection2',NlpSegmentDb.link_id_subsection2)
Index('nlp_segment_db_link_id_subsection3',NlpSegmentDb.link_id_subsection3)
Index('nlp_segment_db_parent_id',NlpSegmentDb.parent_id,NlpSegmentDb.group_type)
Index('nlp_segment_db_parent_id_hierarchy',NlpSegmentDb.parent_id,NlpSegmentDb.hierarchy,NlpSegmentDb.group_type)
